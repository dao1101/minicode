import json
import math
from pathlib import Path
from typing import List, Dict, Any, Optional

from minicode.sessions.store import SESSIONS_DIR, save_session
from minicode.llm.client import ModelClient


def _session_text(messages: List[Dict[str, Any]], max_chars: int = 2000) -> str:
    lines = []
    total = 0
    for m in messages:
        text = str(m.get("content", "") or "")
        if total + len(text) > max_chars:
            text = text[: max_chars - total]
            lines.append(text)
            break
        lines.append(text)
        total += len(text)
    return "\n".join(lines)


def save_session_with_embedding(
    llm: ModelClient, title: str, messages: List[Dict[str, Any]]
) -> Dict:
    meta = save_session(title, messages)
    session_id = meta["id"]
    path = SESSIONS_DIR / f"{session_id}.json"
    try:
        text = _session_text(messages)
        embedding = llm.embed(text)
        data = json.loads(path.read_text(encoding="utf-8"))
        data["embedding"] = embedding
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    except Exception as e:
        print(f"[RAG] Embedding failed for session {session_id}: {e}")
    return meta


def cosine_similarity(a: List[float], b: List[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


# TODO: 遍历全量 session 文件做余弦相似度，session 数超过 100 后建议换向量数据库
def search_semantic(
    llm: ModelClient, query: str, top_k: int = 5
) -> List[Dict[str, Any]]:
    try:
        query_embedding = llm.embed(query)
    except Exception as e:
        print(f"[RAG] Query embedding failed: {e}")
        return []

    scored = []
    for p in sorted(
        SESSIONS_DIR.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True
    ):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            embedding = data.get("embedding")
            if not embedding:
                continue
            score = cosine_similarity(query_embedding, embedding)
            meta = data.get("meta", {})
            meta["_score"] = round(score, 4)
            scored.append(meta)
        except Exception:
            continue

    scored.sort(key=lambda x: x["_score"], reverse=True)
    return scored[:top_k]
