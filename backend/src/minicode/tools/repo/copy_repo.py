import os
import threading
from pathlib import Path
import shutil
from minicode.tools.decorator import tool
from minicode.tools.ignore import should_ignore

_TIMEOUT = 30


def _run_with_timeout(fn, *args, timeout=_TIMEOUT) -> bool:
    result = []
    exc = []

    def worker():
        try:
            result.append(fn(*args))
        except Exception as e:
            exc.append(e)

    t = threading.Thread(target=worker, daemon=True)
    t.start()
    t.join(timeout)

    if t.is_alive():
        return False
    if exc:
        return False
    return True


@tool
def copy_repo(src: str = ".", dst: str = ""):
    """
    Backup repository to destination, filtering by .gitignore

    src: source repo directory path
    dst: destination directory path (default: ~/Desktop/{src_name}_copy)
    """
    src_path = Path(src).resolve()
    if not dst:
        dst = str(Path.home() / "Desktop" / f"{src_path.name}_copy")
    dst_path = Path(dst).resolve()

    if dst_path.exists():
        if not _run_with_timeout(shutil.rmtree, dst_path):
            return f"Failed to remove existing destination: {dst}"

    copied = 0
    failed = 0
    for current_root, dirs, files in os.walk(src_path):
        current = Path(current_root)

        try:
            dirs[:] = [d for d in dirs if not should_ignore(current / d, src_path)]
        except Exception:
            pass

        for name in files:
            path = current / name
            try:
                if should_ignore(path, src_path):
                    continue
            except Exception:
                continue

            rel = os.path.relpath(path, src_path).replace("\\", "/")
            dest = dst_path / rel
            try:
                dest.parent.mkdir(parents=True, exist_ok=True)
            except Exception:
                continue

            if _run_with_timeout(shutil.copy, path, dest):
                copied += 1
            else:
                failed += 1

        for name in dirs:
            path = current / name
            rel = os.path.relpath(path, src_path).replace("\\", "/")
            dest = dst_path / rel
            try:
                dest.mkdir(parents=True, exist_ok=True)
            except Exception:
                pass

    msg = f"Copied {copied} files to {dst}"
    if failed:
        msg += f" ({failed} files skipped due to errors)"
    return msg
