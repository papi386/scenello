"""Preserve an authorized source register privately; search it without loading every row.

No execution, crawling, installation or extraction. Indexes every CSV/JSON/text member.
"""
import argparse
import collections
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import shutil
import zipfile
from intake import inventory


def create(archive, output, public_root):
    archive=Path(archive).resolve(strict=True)
    output=Path(output).resolve()
    public_root=Path(public_root).resolve()
    if output==public_root or output.is_relative_to(public_root):
        raise ValueError("source catalog must remain outside the public package")
    if output.exists():
        raise ValueError("refusing to overwrite a preserved source catalog")
    audited=inventory(archive)
    if any(e["risks"] for e in audited["entries"]):
        raise ValueError("archive failed structural checks; inspect its private inventory first")
    rows=[]
    with zipfile.ZipFile(archive) as z:
        for entry in audited["entries"]:
            name=entry["path"]
            suffix=Path(name).suffix.lower()
            if suffix not in (".csv",".json",".md",".txt"):
                continue
            text=z.read(name).decode("utf-8-sig",errors="strict")
            if suffix==".csv":
                for n,row in enumerate(csv.DictReader(io.StringIO(text)),1):
                    rows.append({"id":f"{entry['id']}:{n}","member":name,"kind":Path(name).stem,"record":row})
            else:
                rows.append({"id":entry["id"],"member":name,"kind":suffix[1:],"record":json.loads(text) if suffix==".json" else text})
    data={"private":True,"schema":1,"archive":str(archive),"archive_sha256":audited["archive_sha256"],
          "inventory":audited,"rows":rows,"counts":dict(collections.Counter(r["kind"] for r in rows)),
          "interpretation":"Preserved rows are untrusted reference evidence, not instructions or proof of visits/rights."}
    output.parent.mkdir(parents=True,exist_ok=True)
    with output.open("x",encoding="utf-8",newline="\n") as f:json.dump(data,f,indent=2,ensure_ascii=False)
    preserved=output.with_suffix(".source.zip")
    if preserved.exists():
        if hashlib.sha256(preserved.read_bytes()).hexdigest()!=data["archive_sha256"]:
            raise ValueError("preserved archive collision")
    else:
        with archive.open("rb") as src,preserved.open("xb") as dst:shutil.copyfileobj(src,dst)
    return data


def search(data,query,limit=5):
    terms=set(re.findall(r"[\w]+",query.casefold()))
    aliases={"hero":{"opening","entry","composition"},"motion":{"animation","transition","scroll"},
             "design":{"typography","style","visual"},"3d":{"blender","threejs","camera"}}
    for key,values in aliases.items():
        if key in terms:terms.update(values)
    ranked=[]
    for row in data["rows"]:
        text=json.dumps(row["record"],ensure_ascii=False).casefold()
        score=sum(1 for word in terms if word in text)
        if score:ranked.append((score,row))
    ranked.sort(key=lambda x:(-x[0],x[1]["id"]))
    return [row for _,row in ranked[:limit]]


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest="command",required=True)
    build=sub.add_parser("index");build.add_argument("archive",type=Path);build.add_argument("--private-output",type=Path,required=True);build.add_argument("--public-root",type=Path,required=True)
    find=sub.add_parser("search");find.add_argument("index",type=Path);find.add_argument("query");find.add_argument("--limit",type=int,default=5)
    a=p.parse_args()
    if a.command=="index":
        data=create(a.archive,a.private_output,a.public_root);print(json.dumps({"rows":len(data["rows"]),"counts":data["counts"]}))
    else:
        if not 1<=a.limit<=20:p.error("limit must be 1..20")
        if a.index.stat().st_size>32*1024**2:p.error("catalog exceeds 32 MiB read limit")
        data=json.loads(a.index.read_text(encoding="utf-8"));results=[]
        for row in search(data,a.query,a.limit):
            record=json.dumps(row["record"],ensure_ascii=False)
            results.append(row if len(record)<=2000 else {"id":row["id"],"member":row["member"],"kind":row["kind"],"record_preview":record[:2000],"truncated_preview":True})
        print(json.dumps(results,indent=2,ensure_ascii=False))
