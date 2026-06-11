import os
from pathlib import Path
from pathspec import PathSpec
from pathspec.patterns.gitwildmatch import GitWildMatchPattern

_git_spec_cache: dict[Path, PathSpec] = {}


def load_gitignore(root: Path) -> PathSpec:
    lines = []
    try:
        gitignore_path = root / ".gitignore"
        if gitignore_path.exists():
            lines = gitignore_path.read_text(encoding="utf-8").splitlines()
    except Exception:
        lines = []
    try:
        return PathSpec.from_lines(GitWildMatchPattern, lines)
    except Exception:
        return PathSpec.from_lines(GitWildMatchPattern, [])


def should_ignore(file_path: Path, root: Path) -> bool:
    try:
        if root not in _git_spec_cache:
            _git_spec_cache[root] = load_gitignore(root)
        rel_path = os.path.relpath(file_path, root).replace("\\", "/")
        if file_path.is_dir():
            rel_path += "/"
        return _git_spec_cache[root].match_file(rel_path)
    except Exception:
        return False
