from typing import List, Dict, Any

from minicode.llm.client import ModelClient
from minicode.sessions.rag_store import search_semantic
from minicode.sessions.store import get_session


def retrieve_context(
    llm: ModelClient,
    query: str,
    top_k: int = 3,
    max_chars: int = 2000,
) -> str:
    results = search_semantic(llm, query, top_k=top_k)
    if not results:
        return ""

    blocks = []
    total = 0

    for r in results:
        session_id = r.get("id")
        if not session_id:
            continue
        data = get_session(session_id)
        if not data:
            continue

        lines = []
        for m in data.get("messages", []):
            role = m.get("role", "?")
            content = str(m.get("content", "") or "")
            lines.append(f"{role}：{content}")

        block = "\n".join(lines)
        if total + len(block) > max_chars:
            block = block[: max_chars - total]
            blocks.append(block)
            break
        blocks.append(block)
        total += len(block)

    if not blocks:
        return ""

    text = "\n━━━━━━━━━━━━━━━━━━━━━━━\n".join(blocks)
    return f"[相关历史会话]\n{text}"
