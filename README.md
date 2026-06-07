# MiniCode

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Vue 3](https://img.shields.io/badge/vue-3.5-4fc08d.svg)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.135+-009688.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

MiniCode is a lightweight, local-first AI coding assistant with streaming chat, a tool-driven agent loop, and **Retrieval-Augmented Generation (RAG)** for cross-session memory. It combines a Vue 3 frontend with a FastAPI backend and supports multiple LLM providers (Qwen, GLM, DeepSeek) with automatic failover.

---

## Features

- **Streaming Chat** — Real-time token-by-token responses over Server-Sent Events.
- **RAG-Powered Long-Term Memory** — Automatically embeds and indexes past conversations. Subsequent queries retrieve semantically relevant context across sessions without manual pasting.
- **Dual Modes** — `build` mode with full tool access vs. `plan` mode with read-only safety.
- **Multi-Provider Routing** — Configurable primary and fallback LLM providers (Qwen, GLM, DeepSeek). If the primary fails, the fallback takes over seamlessly.
- **Extensible Tool System** — Tools are auto-discovered from the `tools/` package. Add a module and it becomes available to the agent.
- **Code-First UI** — Built-in file tree browser, Monaco code editor, and streaming diff viewer.
- **Zero Database** — All sessions, messages, and embeddings are stored as flat JSON files. No external vector database required — embeddings are served by the LLM provider's API.

> See [Design Decisions](#design-decisions) for rationale behind key architectural choices.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Vue 3 Frontend                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────────────┐  │
│  │ FileTree │  │  Editor  │  │  Chat Panel              │  │
│  │ Sidebar  │  │  Monaco  │  │  ┌────┐ ┌────┐ ┌──────┐│  │
│  │          │  │          │  │  │User│ │Agent│ │RAG   ││  │
│  │          │  │          │  │  │    │ │    │ │Toggle││  │
│  └──────────┘  └──────────┘  │  └────┘ └────┘ └──────┘│  │
│                               └──────────────────────────┘  │
└──────────────────────┬──────────────────────────────────────┘
                       │ POST /chat  (SSE stream)
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                           │
│                                                              │
│  ┌─────────────┐    ┌──────────────┐    ┌────────────────┐  │
│  │  /chat      │───▶│ Router       │───▶│ Agent           │  │
│  │  /sessions  │    │ (primary /   │    │ (memory + tools)│  │
│  │  /sessions/ │    │  fallback)   │    └────────────────┘  │
│  │    search   │    └──────────────┘           │             │
│  └──────┬──────┘                               │             │
│         │                                      ▼             │
│         │                               ┌────────────────┐  │
│         │                               │ Plan Generator │  │
│         │                               │ + Builder      │  │
│         │                               └────────────────┘  │
│         │                                      │             │
│         ▼                                      ▼             │
│  ┌──────────────┐                     ┌────────────────┐  │
│  │ RAG Retriever│                    │ Tool Registry   │  │
│  │ embed query  │                     │ + Runner        │  │
│  │ → cosine sim │                     │ (read, write,   │  │
│  │ → inject ctx │                     │  search, ...)   │  │
│  └──────┬───────┘                    └────────────────┘  │
│         │                                                  │
│         ▼                                                  │
│  ┌──────────────┐                                          │
│  │  Sessions    │  (.minicode/sessions/*.json)             │
│  │  + Embedding │  {meta, messages, embedding: [...]}      │
│  └──────────────┘                                          │
└─────────────────────────────────────────────────────────────┘
```

### RAG Flow

1. User toggles `🧠 RAG` on in the chat panel.
2. On each message, the backend embeds the query via the LLM provider's embedding API.
3. Cosine similarity is computed against all saved session embeddings.
4. The top-K matching sessions are retrieved and their raw messages are injected into the prompt.
5. Retrieved messages are injected as plain text; raw embedding vectors are never sent to the model.
6. The LLM responds with relevant context.

---

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 20+
- An API key for at least one supported provider

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
# Optional: create backend/.env with your API keys
```

### Frontend

```bash
cd frontend/vue
npm install
```

### Launch

```bash
minicode
```

After installing the backend with `pip install -e .`, the `minicode` CLI starts both the backend (port 8000) and frontend (port 5173) simultaneously and opens the browser.

To start the backend alone:

```bash
python -m minicode.main
```

---

## Configuration

Set these in `backend/.env` (or export as environment variables):

| Variable | Default | Description |
|----------|---------|-------------|
| `PRIMARY_PROVIDER` | `deepseek` | Primary LLM provider (`qwen`, `glm`, `deepseek`) |
| `FALLBACK_PROVIDER` | `qwen` | Fallback on primary failure |
| `EMBEDDING_PROVIDER` | `qwen` | Provider used for RAG embeddings (`qwen` or `glm`) |
| `QWEN_API_KEY` | — | API key for Qwen |
| `GLM_API_KEY` | — | API key for GLM |
| `DEEPSEEK_API_KEY` | — | API key for DeepSeek |

Full reference in `backend/src/minicode/config.py`.

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Health check |
| `GET` | `/ping` | Status probe |
| `POST` | `/chat` | Send message (`mode`: `build`/`plan`, `rag`: `true`/`false`) |
| `GET` | `/sessions` | List sessions, optional `?q=` keyword filter |
| `GET` | `/sessions/search` | Search sessions (`?q=&semantic=true`) |
| `POST` | `/sessions` | Save current conversation |
| `GET` | `/sessions/{id}` | Load a saved session |
| `DELETE` | `/sessions/{id}` | Delete a session |

---

## Project Structure

```
backend/src/minicode/
├── main.py              # FastAPI app, routing, RAG integration
├── config.py            # Environment config & agent limits
├── core/                # Agent & Controller orchestration
├── llm/                 # Provider clients, router, embedding
├── memory/              # Conversation context management
├── plan/                # Plan generator & step builder
├── runtime/             # Step controller & execution guards
├── tools/               # Auto-loaded tool implementations
└── sessions/            # Session storage & RAG retriever

frontend/vue/src/
├── api/                 # API client (chat, sessions)
├── components/          # Chat, Editor, Sidebar, FileTree
└── stores/              # Reactive state (uiState, uiActions)
```

---

## Design Decisions

- **File-based storage** — Sessions are JSON files. For a local single-user tool this avoids database setup, keeps data portable, and makes manual inspection trivial.
- **API-based embeddings** — Rather than running a local embedding model (sentence-transformers), the system reuses the configured LLM provider's embedding endpoint. Zero additional dependencies.
- **RAG injection at the prompt level** — Retrieved context is prepended to the user message before it enters the agent loop. No changes to the agent's internal memory model are needed.
- **Scoped `withTimeout`** — All frontend API calls use `AbortController` with a 10-second timeout to prevent hanging requests when embedding or LLM calls stall.

---

## License

MIT
