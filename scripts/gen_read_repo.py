from pathlib import Path
from src.tools.repo.read_repo import read_repo


if __name__ == "__main__":
    path1 = r"C:\Users\hhy\Desktop\minicode\frontend\vue\src"
    path2 = r"C:\Users\hhy\Desktop\minicode\backend\src"

    result = read_repo(path2) #+ "\n" + read_repo(path2)

    Path(r"docs\read_repo.txt").write_text(result, encoding="utf-8")

    print("\n===== REPO CONTENT =====\n")
    print("read_repo.txt已生成")
