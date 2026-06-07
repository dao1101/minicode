from pathlib import Path
from src.tools.repo.repo_map import repo_map


if __name__ == "__main__":
    result = repo_map(r"C:\Users\hhy\Desktop\minicode\backend\minicode")

    Path(r"docs\repo_map.txt").write_text(result, encoding="utf-8")

    print("\n===== REPO MAP =====\n")
    print("repo_map.txt已生成")
