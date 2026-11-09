"""Copy the canonical skill into one explicitly selected project; never global config.

Default is a dry run. Existing installations are never overwritten or deleted.
"""
import argparse
from pathlib import Path
import shutil

SOURCE=Path(__file__).resolve().parents[1]/"skills/scenello"


def install(project, agent="codex", apply=False):
    project=Path(project).resolve(strict=True)
    if not project.is_dir():
        raise ValueError("target must be an existing project directory")
    container=project/(".agents" if agent=="codex" else ".claude")/"skills"
    target=container/"scenello"
    for parent in (project,container.parent,container,target):
        if parent.is_symlink() or not parent.resolve().is_relative_to(project):
            raise ValueError("symlinked or escaping install destination")
    if target.exists():
        raise ValueError("existing skill: review and archive it manually before updating")
    if apply:
        container.mkdir(parents=True,exist_ok=True)
        shutil.copytree(SOURCE,target,ignore=shutil.ignore_patterns("__pycache__","*.pyc"))
    return target


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("project",type=Path)
    p.add_argument("--agent",choices=("codex","claude"),default="codex")
    p.add_argument("--apply",action="store_true")
    a=p.parse_args()
    print(("Copied to " if a.apply else "Would copy to ")+str(install(a.project,a.agent,a.apply)))
