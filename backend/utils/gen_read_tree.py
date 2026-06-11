from pathlib import Path
from minicode.tools.repo.read_tree import read_tree


if __name__ == "__main__":
    # project root e.g. ~/Desktop/minicode
    root = Path(__file__).resolve().parent.parent.parent
    result = read_tree(str(root))

    docs_dir = Path(__file__).resolve().parent.parent.parent / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    (docs_dir / "read_tree.txt").write_text(result, encoding="utf-8")

    print("\n===== TREE =====\n")
    print("read_tree.txt generated")
