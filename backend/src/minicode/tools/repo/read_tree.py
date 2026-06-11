from pathlib import Path
from minicode.tools.decorator import tool
from minicode.tools.ignore import should_ignore


@tool
def read_tree(path: str):
    """
    Read project directory tree

    Args:
        path: project root path
    """

    root = Path(path)

    if not root.exists():
        return "Path not found"

    if not root.is_dir():
        return "Path is not a directory"

    lines = []
    lines.append(f"{root.name}/")

    def get_children(current: Path):
        try:
            children = list(current.iterdir())
        except Exception:
            return []

        filtered = []
        for c in children:
            try:
                if not should_ignore(c, root):
                    filtered.append(c)
            except Exception:
                continue

        return sorted(filtered, key=lambda x: x.name)

    def traverse(current: Path, prefix: str = "", seen: set = None):
        if seen is None:
            seen = set()
        real = current.resolve()
        if real in seen:
            lines.append(f"{prefix}└── {current.name}/ (symlink loop)")
            return
        seen.add(real)

        children = get_children(current)
        total = len(children)

        for i, child in enumerate(children):
            is_last = i == total - 1
            connector = "└── " if is_last else "├── "

            lines.append(
                f"{prefix}{connector}{child.name}{'/' if child.is_dir() else ''}"
            )

            if child.is_dir():
                new_prefix = prefix + ("    " if is_last else "│   ")
                traverse(child, new_prefix, seen.copy())

    traverse(root)

    return "\n".join(lines)
