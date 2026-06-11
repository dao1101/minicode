from pathlib import Path
from minicode.tools.repo.repo_map import repo_map


if __name__ == "__main__":
    # project root e.g. ~/Desktop/minicode
    root = Path(__file__).resolve().parent.parent.parent
    result = repo_map(str(root))

    docs_dir = Path(__file__).resolve().parent.parent.parent / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    (docs_dir / "repo_map.txt").write_text(result, encoding="utf-8")

    print("\n===== REPO MAP =====\n")
    print("repo_map.txt generated")
