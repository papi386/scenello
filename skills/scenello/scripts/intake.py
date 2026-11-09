"""Inventory ZIPs without extraction or execution. Output is PRIVATE, not a release asset.

No recursive archive expansion. Bounded streaming hashes check CRCs through ZipFile.
Central-directory metadata is evidence, not proof that a file is safe or licensed.
"""
import argparse
import collections
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import unicodedata
import zipfile

DISPOSITIONS = ("PUBLIC_REUSABLE", "PUBLIC_LINK_ONLY", "SAFE_DERIVATION",
                "PRIVATE_REFERENCE_ONLY", "OUT_OF_SCOPE", "UNVERIFIED", "REJECTED_UNSAFE")
ARCHIVES = {".zip", ".7z", ".rar", ".tar", ".gz", ".bz2", ".xz"}
EXECUTABLE = {".exe", ".dll", ".com", ".bat", ".cmd", ".ps1", ".sh", ".msi", ".scr", ".py", ".js", ".mjs", ".html", ".blend"}


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def path_risks(name):
    normalized = unicodedata.normalize("NFC", name.replace("\\", "/"))
    parts = normalized.rstrip("/").split("/")
    problems = []
    if normalized.startswith("/") or re.match(r"^[A-Za-z]:", normalized):
        problems.append("absolute-path")
    if any(p in (".", "..", "") for p in parts):
        problems.append("ambiguous-or-traversal-path")
    if any(":" in p or p.endswith((" ", ".")) for p in parts):
        problems.append("windows-path-alias-or-stream")
    if any(re.match(r"^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\.|$)", p, re.I) for p in parts):
        problems.append("reserved-device-name")
    if any(unicodedata.category(c) in ("Cc", "Cf") for c in normalized):
        problems.append("control-character")
    if len(name) > 1024 or len(parts) > 40:
        problems.append("path-limit")
    return normalized.casefold(), problems


def inventory(archive, *, max_entries=10000, max_total=1024**3,
              max_member=128*1024**2, max_ratio=250):
    archive = Path(archive).resolve(strict=True)
    if archive.stat().st_size > max_total:
        raise ValueError("archive exceeds input byte limit")
    result = {"schema": 1, "private": True, "archive": str(archive),
              "archive_sha256": digest(archive), "entries": []}
    with zipfile.ZipFile(archive) as z:
        infos = z.infolist()
        if len(infos) > max_entries:
            raise ValueError("entry count limit exceeded")
        if sum(i.file_size for i in infos) > max_total:
            raise ValueError("declared expansion limit exceeded")
        regular_paths = {path_risks(i.filename)[0].rstrip("/") for i in infos if not i.is_dir()}
        conflicts = set()
        for i in infos:
            key = path_risks(i.filename)[0].rstrip("/")
            parts = key.split("/")
            for n in range(1, len(parts)):
                parent = "/".join(parts[:n])
                if parent in regular_paths:
                    conflicts.update((parent, key))
        seen = set()
        streamed = 0
        for index, info in enumerate(infos):
            key, risks = path_risks(info.filename)
            if key.rstrip("/") in conflicts:
                risks.append("file-directory-conflict")
            if key in seen:
                risks.append("duplicate-or-case-collision")
            seen.add(key)
            mode = info.external_attr >> 16
            if stat.S_ISLNK(mode) or (stat.S_IFMT(mode) not in (0, stat.S_IFREG, stat.S_IFDIR)):
                risks.append("link-or-special-file")
            if info.flag_bits & 1:
                risks.append("encrypted")
            if info.file_size > max_member:
                risks.append("member-byte-limit")
            if info.file_size / max(1, info.compress_size) > max_ratio:
                risks.append("expansion-ratio")
            suffix = PurePosixPath(info.filename).suffix.lower()
            if suffix in ARCHIVES:
                risks.append("nested-archive-not-expanded")
            # Code is inventoried, never imported or run.
            entry = {"id": f"entry-{index+1:05d}", "path": info.filename,
                     "bytes": info.file_size, "compressed_bytes": info.compress_size,
                     "risks": risks, "executable_or_active": suffix in EXECUTABLE,
                     "disposition": "REJECTED_UNSAFE" if risks else "UNVERIFIED",
                     "license": "unknown", "review": "metadata only", "sha256": None}
            if not risks and not info.is_dir():
                h = hashlib.sha256()
                count = 0
                with z.open(info) as f:
                    while chunk := f.read(1024 * 1024):
                        count += len(chunk)
                        streamed += len(chunk)
                        if count > max_member or streamed > max_total:
                            raise ValueError("actual expansion limit exceeded")
                        h.update(chunk)
                if count != info.file_size:
                    raise ValueError("member length mismatch")
                entry["sha256"] = h.hexdigest()
            result["entries"].append(entry)
    result["counts"] = dict(collections.Counter(e["disposition"] for e in result["entries"]))
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("archive", type=Path)
    p.add_argument("--private-output", type=Path, required=True)
    p.add_argument("--public-root", type=Path, required=True)
    args = p.parse_args()
    target = args.private_output.resolve()
    root = args.public_root.resolve()
    if target == root or root in target.parents:
        p.error("private inventory must stay outside public repository")
    if target.exists():
        p.error("refusing to overwrite an existing ledger")
    if shutil.disk_usage(target.parent).free < 32*1024**2:
        p.error("insufficient free disk reserve")
    data = inventory(args.archive)
    with target.open("x", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(json.dumps({"entries": len(data["entries"]), "counts": data["counts"]}))


if __name__ == "__main__":
    main()
