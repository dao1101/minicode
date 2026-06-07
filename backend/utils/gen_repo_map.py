from pathlib import Path
from minicode.tools.repo.repo_map import repo_map


if __name__ == "__main__":
    result = repo_map(r"C:\Users\hhy\Desktop\minicode")

    docs_dir = Path(__file__).resolve().parent.parent / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    (docs_dir / "repo_map.txt").write_text(result, encoding="utf-8")

    print("\n===== REPO MAP =====\n")
    print("repo_map.txt generated")
