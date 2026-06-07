from pathlib import Path
from pathspec import PathSpec
from pathspec.patterns.gitwildmatch import GitWildMatchPattern

_git_spec_cache: dict[Path, PathSpec] = {}


def load_gitignore(root: Path) -> PathSpec:
    gitignore_path = root / ".gitignore"
    lines = []
    if gitignore_path.exists():
        lines = gitignore_path.read_text(encoding="utf-8").splitlines()
    return PathSpec.from_lines(GitWildMatchPattern, lines)


def should_ignore(file_path: Path, root: Path) -> bool:
    if root not in _git_spec_cache:
        _git_spec_cache[root] = load_gitignore(root)
    rel_path = file_path.relative_to(root).as_posix()
    if file_path.is_dir():
        rel_path += "/"
    return _git_spec_cache[root].match_file(rel_path)
