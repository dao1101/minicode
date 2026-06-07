from pathlib import Path
from pathspec import PathSpec
from pathspec.patterns.gitwildmatch import GitWildMatchPattern
import shutil
from minicode.tools.decorator import tool


@tool
def copy_repo(src: str = ".", dst: str = ""):
    """
    Backup repository to destination, filtering by .gitignore

    src: source repo directory path
    dst: destination directory path (default: ~/Desktop/{src_name}_copy)
    """
    src_path = Path(src).resolve()
    if not dst:
        dst = str(Path.home() / "Desktop" / f"{src_path.name}_copy")
    dst_path = Path(dst).resolve()

    gitignore = src_path / ".gitignore"
    spec = PathSpec.from_lines(
        GitWildMatchPattern,
        gitignore.read_text(encoding="utf-8").splitlines()
        if gitignore.exists()
        else [],
    )

    if dst_path.exists():
        shutil.rmtree(dst_path)

    copied = 0
    for path in src_path.rglob("*"):
        try:
            rel = path.relative_to(src_path).as_posix()
        except (AttributeError, ValueError):
            continue

        parent = path.parent
        skip = False
        while parent != src_path:
            try:
                prel = parent.relative_to(src_path).as_posix() + "/"
            except (AttributeError, ValueError):
                skip = True
                break
            if spec.match_file(prel):
                skip = True
                break
            parent = parent.parent
        if skip:
            continue

        match_path = rel + "/" if path.is_dir() else rel
        if spec.match_file(match_path):
            continue

        dest = dst_path / rel
        if path.is_dir():
            dest.mkdir(parents=True, exist_ok=True)
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            try:
                shutil.copy(path, dest)
                copied += 1
            except shutil.SameFileError:
                pass

    return f"Copied {copied} files to {dst}"
