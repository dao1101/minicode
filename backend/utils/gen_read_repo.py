from pathlib import Path
from minicode.tools.repo.read_repo import read_repo


if __name__ == "__main__":
    path = r"C:\Users\hhy\Desktop\minicode"

    result = read_repo(path)

    docs_dir = Path(__file__).resolve().parent.parent / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    (docs_dir / "read_repo.txt").write_text(result, encoding="utf-8")

    print("\n===== REPO CONTENT =====\n")
    print("read_repo.txt generated")
