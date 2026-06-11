import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env located at the repository backend directory (robust to working dir)
env_path = Path(__file__).resolve().parents[2] / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=str(env_path))
else:
    # fallback to default behavior
    load_dotenv()

__all__ = [
    "QWEN_ENDPOINT",
    "QWEN_API_KEY",
    "QWEN_MODEL",
    "QWEN_EMBED_ENDPOINT",
    "QWEN_EMBED_MODEL",
    "GLM_EMBED_ENDPOINT",
    "GLM_EMBED_MODEL",
    "GLM_ENDPOINT",
    "GLM_API_KEY",
    "GLM_MODEL",
    "DEEPSEEK_ENDPOINT",
    "DEEPSEEK_API_KEY",
    "DEEPSEEK_MODEL",
    "PRIMARY_PROVIDER",
    "FALLBACK_PROVIDER",
    "EMBEDDING_PROVIDER",
    "PROVIDERS",
    "MAX_TOOL_LOOP",
    "MAX_STEP",
    "MEMORY_LIMIT",
    "MEMORY_FILE",
    "SAFE_TOOLS",
]

# =========================
# LLM Providers
# =========================
PROVIDERS = ["qwen", "glm", "deepseek"]


QWEN_ENDPOINT = os.getenv("QWEN_ENDPOINT", "")
QWEN_API_KEY = os.getenv("QWEN_API_KEY", "")
QWEN_MODEL = os.getenv("QWEN_MODEL", "qwen-plus")

QWEN_EMBED_ENDPOINT = os.getenv("QWEN_EMBED_ENDPOINT", "")
QWEN_EMBED_MODEL = os.getenv("QWEN_EMBED_MODEL", "text-embedding-v3")

GLM_ENDPOINT = os.getenv("GLM_ENDPOINT", "")
GLM_API_KEY = os.getenv("GLM_API_KEY", "")
GLM_MODEL = os.getenv("GLM_MODEL", "glm-4")

GLM_EMBED_ENDPOINT = os.getenv("GLM_EMBED_ENDPOINT", "")
GLM_EMBED_MODEL = os.getenv("GLM_EMBED_MODEL", "embedding-3")


DEEPSEEK_ENDPOINT = os.getenv("DEEPSEEK_ENDPOINT", "")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-v4-flash")


# =========================
# Router
# =========================

PRIMARY_PROVIDER = os.getenv("PRIMARY_PROVIDER", "deepseek")
FALLBACK_PROVIDER = os.getenv("FALLBACK_PROVIDER", "qwen")
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "qwen")

# =========================
# Agent Limits
# =========================

MAX_TOOL_LOOP = 4
MAX_STEP = 4


# =========================
# Memory
# =========================

MEMORY_LIMIT = 50
MEMORY_FILE = ".memory.json"


# =========================
# Safe Tools (Plan Mode)
# =========================
SAFE_TOOLS = {
    "read_file",
    "read_range",
    "read_tree",
    "read_repo",
    "repo_map",
    "grep",
    "search_file",
    "search_symbol",
    "list_dir",
    "web_search",
    "web_fetch",
}
