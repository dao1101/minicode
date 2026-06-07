import argparse
from pathlib import Path
from minicode.tools.repo.copy_repo import copy_repo


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    src_default = str(Path.home() / "Desktop" / "minicode")
    dst_default = str(Path.home() / "Desktop" / "minicode_copy")
    parser.add_argument("--src", default=src_default)
    parser.add_argument("--dst", default=dst_default)
    args = parser.parse_args()

    result = copy_repo(args.src, args.dst)
    print(result)
