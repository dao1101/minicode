from pathlib import Path
from src.tools.repo.read_tree import read_tree


if __name__ == "__main__":
    result = read_tree(r"C:\Users\hhy\Desktop\minicode\frontend")

    Path(r"docs\read_tree.txt").write_text(result, encoding="utf-8")

    print("\n===== TREE =====\n")
    print("read_tree.txt已生成")
