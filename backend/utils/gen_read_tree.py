from pathlib import Path
from minicode.tools.repo.read_tree import read_tree


if __name__ == "__main__":
    result = read_tree(r"C:\Users\hhy\Desktop\minicode")

    docs_dir = Path(__file__).resolve().parent.parent / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    (docs_dir / "read_tree.txt").write_text(result, encoding="utf-8")

    print("\n===== TREE =====\n")
    print("read_tree.txt generated")
