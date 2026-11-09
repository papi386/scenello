"""Offline suggestions for selected references, not a host skill activation test."""
import argparse
import json
from pathlib import Path
import re

INDEX = Path(__file__).resolve().parents[1] / "references" / "techniques.json"


def route(query):
    words = set(re.findall(r"[a-z0-9]+", query.lower()))
    # An editing-only request belongs elsewhere. Mixed requests still need judgement.
    editing = words & {"reel", "montage", "soundtrack", "ffmpeg", "hyperframes"}
    web = words & {"website", "web", "page", "browser", "portfolio"}
    if editing and not web:
        return {"scope": "outside", "references": [], "reason": "video production request"}
    entries = json.loads(INDEX.read_text(encoding="utf-8"))
    # Intent phrases prioritize the mechanism over generic words such as camera.
    normalized = " ".join(re.findall(r"[a-z0-9]+", query.lower()))
    intents = [
        (("shared image", "shared element", "image to detail", "architecture", "architectural"), {"SCN-02": 7, "SCN-07": 4}),
        (("continuous journey", "continuous camera", "travel through", "three worlds", "immersive"), {"SCN-09": 8, "SCN-10": 6, "SCN-06": 4}),
        (("lamp", "pbr", "material", "metal", "studio lighting", "finish change"), {"SCN-16": 8, "SCN-06": 6, "SCN-15": 4}),
        (("festival", "schedule", "filter", "program interface", "dock"), {"SCN-21": 8, "SCN-02": 6}),
        (("stutter", "startup spike", "latency", "p95", "p99"), {"SCN-04": 12}),
    ]
    boosts = {}; reasons = {}
    for phrases, weights in intents:
        matched = [phrase for phrase in phrases if re.search(r"\b" + re.escape(phrase) + r"\b", normalized)]
        if matched:
            for identifier, weight in weights.items():
                boosts[identifier] = boosts.get(identifier, 0) + weight
                reasons.setdefault(identifier, []).extend(matched)
    ranked = sorted(((len(words.intersection(e["tags"])) + boosts.get(e["id"], 0), e) for e in entries),
                    key=lambda pair: (-pair[0], pair[1]["id"]))
    matches = [dict(e, route_score=score, matched_intents=reasons.get(e["id"], [])) for score, e in ranked if score > 0][:3]
    substantial = bool(words & {"rebuild", "rejected", "cinematic", "photorealistic", "immersive"})
    return {"scope": "web" if matches else "unresolved", "references": matches,
            "workflow": (["creative-production.md", "creative-validation.md", "skills-and-mcps.md"] if substantial and words & {"full", "entire", "immersive", "rebuild"} else ["art-direction.md", "motion.md"] if substantial else []),
            "evidence_required": "Inspect actual sources; a suggested module is not proof of inspection or successful implementation.",
            "limitation": "Lexical offline routing only. Verify host skill activation with actual agent events separately."}



if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("query")
    print(json.dumps(route(p.parse_args().query), indent=2))
