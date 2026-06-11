import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional


def _sessions_dir() -> Path:
    import os

    custom = os.getenv("MINICODE_SESSIONS_DIR")
    if custom:
        return Path(custom)
    return Path(__file__).resolve().parent.parent.parent.parent / ".session"


SESSIONS_DIR = _sessions_dir()


def _ensure_dir():
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)


def save_session(title: str, messages: List[Dict[str, Any]]) -> Dict:
    _ensure_dir()
    session_id = str(uuid.uuid4())[:8]
    ts = datetime.now().isoformat(timespec="seconds")
    if not title:
        for m in messages:
            if m.get("role") == "user":
                title = str(m.get("content", ""))[:20] or "会话"
                break
        else:
            title = "会话"

    meta = {"id": session_id, "title": title, "created_at": ts, "count": len(messages)}
    data = {"meta": meta, "messages": messages}

    path = SESSIONS_DIR / f"{session_id}.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return meta


def list_sessions(query: str = "") -> List[Dict]:
    _ensure_dir()
    results = []
    for p in sorted(
        SESSIONS_DIR.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True
    ):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            meta = data.get("meta", {})
            if query:
                hit = query.lower() in meta.get("title", "").lower()
                if not hit:
                    for m in data.get("messages", []):
                        if query.lower() in str(m.get("content", "")).lower():
                            hit = True
                            break
                if not hit:
                    continue
            results.append(meta)
        except Exception:
            continue
    return results


def get_session(session_id: str) -> Optional[Dict]:
    path = SESSIONS_DIR / f"{session_id}.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def delete_session(session_id: str) -> bool:
    path = SESSIONS_DIR / f"{session_id}.json"
    if path.exists():
        path.unlink()
        return True
    return False
