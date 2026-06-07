import subprocess
from minicode.tools.decorator import tool


@tool
def shell_run(cmd: str):
    """
    Execute shell command

    cmd: shell command
    """

    result = subprocess.run(cmd, shell=True, capture_output=True, encoding="utf-8", timeout=30)

    return result.stdout + result.stderr
