# MiniCode

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Vue 3](https://img.shields.io/badge/vue-3.5-4fc08d.svg)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.135+-009688.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

---

## I. Core Project Positioning

MiniCode is a lightweight, local-first AI programming assistant built with Vue3 + FastAPI.
It features streaming dialogue, tool invocation and RAG-powered cross-session memory.
The project supports automatic failover for multiple LLM providers and requires no database. All data is stored in local files.

---

## II. Overall Core Architecture

# My Project

<svg width="100%" viewBox="0 0 680 720" role="img">
  <title>minicode system architecture diagram</title>
  <desc>Vue 3 frontend, FastAPI backend, RAG retriever, session storage, and tool registry with data flow arrows.</desc>
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
  </defs>
  <!-- Frontend -->
<rect x="30" y="24" width="620" height="160" rx="14" fill="#EEEDFE" stroke="#534AB7" stroke-width="0.5"/>
  <text font-family="sans-serif" font-size="14" font-weight="500" fill="#3C3489" x="50" y="50" dominant-baseline="central">Vue 3 Frontend</text>
<rect x="52" y="64" width="150" height="96" rx="8" fill="#EEEDFE" stroke="#534AB7" stroke-width="0.5"/>
  <text font-family="sans-serif" font-size="14" font-weight="500" fill="#3C3489" x="127" y="100" text-anchor="middle" dominant-baseline="central">File tree</text>
  <text font-family="sans-serif" font-size="12" fill="#534AB7" x="127" y="120" text-anchor="middle" dominant-baseline="central">Browse project files</text>
<rect x="226" y="64" width="150" height="96" rx="8" fill="#EEEDFE" stroke="#534AB7" stroke-width="0.5"/>
  <text font-family="sans-serif" font-size="14" font-weight="500" fill="#3C3489" x="301" y="100" text-anchor="middle" dominant-baseline="central">Monaco editor</text>
  <text font-family="sans-serif" font-size="12" fill="#534AB7" x="301" y="120" text-anchor="middle" dominant-baseline="central">Code editing &amp; syntax</text>
<rect x="400" y="64" width="226" height="96" rx="8" fill="#EEEDFE" stroke="#534AB7" stroke-width="0.5"/>
  <text font-family="sans-serif" font-size="14" font-weight="500" fill="#3C3489" x="513" y="95" text-anchor="middle" dominant-baseline="central">Chat panel</text>
  <text font-family="sans-serif" font-size="12" fill="#534AB7" x="513" y="115" text-anchor="middle" dominant-baseline="central">User · Agent · RAG toggle</text>
  <text font-family="sans-serif" font-size="12" fill="#534AB7" x="513" y="133" text-anchor="middle" dominant-baseline="central">SSE streaming output</text>
  <!-- Arrow: frontend → backend -->
<line x1="340" y1="184" x2="340" y2="228" stroke="#888780" stroke-width="1.5" marker-end="url(#arrow)"/>
  <text font-family="sans-serif" font-size="12" fill="#888780" x="356" y="210" dominant-baseline="central">POST /chat (SSE stream)</text>
  <!-- Backend -->
<rect x="30" y="236" width="620" height="300" rx="14" fill="#E1F5EE" stroke="#0F6E56" stroke-width="0.5"/>
  <text font-family="sans-serif" font-size="14" font-weight="500" fill="#085041" x="50" y="262" dominant-baseline="central">FastAPI Backend</text>
<rect x="52" y="276" width="154" height="96" rx="8" fill="#E1F5EE" stroke="#0F6E56" stroke-width="0.5"/>
  <text font-family="sans-serif" font-size="14" font-weight="500" fill="#085041" x="129" y="308" text-anchor="middle" dominant-baseline="central">API routes</text>
  <text font-family="sans-serif" font-size="12" fill="#0F6E56" x="129" y="328" text-anchor="middle" dominant-baseline="central">/chat · /sessions</text>
  <text font-family="sans-serif" font-size="12" fill="#0F6E56" x="129" y="346" text-anchor="middle" dominant-baseline="central">/sessions/search</text>
<rect x="238" y="276" width="154" height="96" rx="8" fill="#E1F5EE" stroke="#0F6E56" stroke-width="0.5"/>
  <text font-family="sans-serif" font-size="14" font-weight="500" fill="#085041" x="315" y="308" text-anchor="middle" dominant-baseline="central">Router</text>
  <text font-family="sans-serif" font-size="12" fill="#0F6E56" x="315" y="328" text-anchor="middle" dominant-baseline="central">Primary / fallback</text>
  <text font-family="sans-serif" font-size="12" fill="#0F6E56" x="315" y="346" text-anchor="middle" dominant-baseline="central">Request dispatch</text>
<rect x="424" y="276" width="202" height="96" rx="8" fill="#E1F5EE" stroke="#0F6E56" stroke-width="0.5"/>
  <text font-family="sans-serif" font-size="14" font-weight="500" fill="#085041" x="525" y="308" text-anchor="middle" dominant-baseline="central">Agent</text>
  <text font-family="sans-serif" font-size="12" fill="#0F6E56" x="525" y="328" text-anchor="middle" dominant-baseline="central">Memory + tool calls</text>
  <text font-family="sans-serif" font-size="12" fill="#0F6E56" x="525" y="346" text-anchor="middle" dominant-baseline="central">Plan &amp; execute</text>
<line x1="206" y1="324" x2="236" y2="324" stroke="#0F6E56" stroke-width="1" marker-end="url(#arrow)"/>
  <line x1="392" y1="324" x2="422" y2="324" stroke="#0F6E56" stroke-width="1" marker-end="url(#arrow)"/>
<rect x="238" y="400" width="154" height="96" rx="8" fill="#E1F5EE" stroke="#0F6E56" stroke-width="0.5"/>
  <text font-family="sans-serif" font-size="14" font-weight="500" fill="#085041" x="315" y="428" text-anchor="middle" dominant-baseline="central">Plan generator</text>
  <text font-family="sans-serif" font-size="12" fill="#0F6E56" x="315" y="448" text-anchor="middle" dominant-baseline="central">Plan + Builder</text>
  <text font-family="sans-serif" font-size="12" fill="#0F6E56" x="315" y="466" text-anchor="middle" dominant-baseline="central">Generate exec steps</text>
<rect x="424" y="400" width="202" height="96" rx="8" fill="#E1F5EE" stroke="#0F6E56" stroke-width="0.5"/>
  <text font-family="sans-serif" font-size="14" font-weight="500" fill="#085041" x="525" y="428" text-anchor="middle" dominant-baseline="central">Tool registry</text>
  <text font-family="sans-serif" font-size="12" fill="#0F6E56" x="525" y="448" text-anchor="middle" dominant-baseline="central">read · write · search</text>
  <text font-family="sans-serif" font-size="12" fill="#0F6E56" x="525" y="466" text-anchor="middle" dominant-baseline="central">Run tool calls</text>
<line x1="525" y1="372" x2="525" y2="398" stroke="#0F6E56" stroke-width="1" marker-end="url(#arrow)"/>
  <line x1="315" y1="372" x2="315" y2="398" stroke="#0F6E56" stroke-width="1" marker-end="url(#arrow)"/>
  <!-- RAG Retriever -->
<rect x="52" y="400" width="154" height="96" rx="8" fill="#FAECE7" stroke="#993C1D" stroke-width="0.5"/>
  <text font-family="sans-serif" font-size="14" font-weight="500" fill="#712B13" x="129" y="428" text-anchor="middle" dominant-baseline="central">RAG retriever</text>
  <text font-family="sans-serif" font-size="12" fill="#993C1D" x="129" y="448" text-anchor="middle" dominant-baseline="central">Embed query</text>
  <text font-family="sans-serif" font-size="12" fill="#993C1D" x="129" y="466" text-anchor="middle" dominant-baseline="central">Cosine sim → inject ctx</text>
<line x1="129" y1="372" x2="129" y2="398" stroke="#0F6E56" stroke-width="1" marker-end="url(#arrow)"/>
  <!-- Arrow: backend → sessions -->
<line x1="362" y1="536" x2="362" y2="570" stroke="#888780" stroke-width="1.5" marker-end="url(#arrow)"/>
  <!-- Sessions -->
<rect x="52" y="572" width="620" height="96" rx="8" fill="#F1EFE8" stroke="#5F5E5A" stroke-width="0.5"/>
  <text font-family="sans-serif" font-size="14" font-weight="500" fill="#2C2C2A" x="362" y="604" text-anchor="middle" dominant-baseline="central">Sessions + embeddings</text>
  <text font-family="sans-serif" font-size="12" fill="#5F5E5A" x="362" y="626" text-anchor="middle" dominant-baseline="central">.minicode/sessions/*.json</text>
  <text font-family="sans-serif" font-size="12" fill="#5F5E5A" x="362" y="646" text-anchor="middle" dominant-baseline="central">{ meta, messages, embedding: [...] }</text>
</svg>

### 1. Layered Architecture

```
Frontend (Vue3) ←SSE Streaming→ Backend (FastAPI) ←API→ Multiple LLM Service Providers
```

- **Frontend**: File tree, Monaco code editor, chat panel, session management
- **Backend**: API routing, LLM routing, intelligent agent, tool system, RAG memory, file storage
- **Storage**: No database. Sessions and embedding vectors are stored in JSON files.

### 2. Core Data Flow

1. User inputs content → Frontend sends SSE streaming request
2. Backend enables RAG (optional) → Retrieve historical session context
3. LLM generates responses with cyclic tool invocation supported
4. Stream results back to frontend → Real-time rendering & tool execution

---

## III. Core Backend Modules

### 1. Configuration Center (`config.py`)

- Unified management for LLM providers, API keys and model parameters
- Define agent constraints (max tool cycles & execution steps)
- Classify secure tools (read-only under Plan mode)

### 2. LLM Management

- **Base Provider Class**: Encapsulate common logic for streaming generation and vector embedding
- **Multi-provider Implementation**: Tongyi Qwen, GLM, DeepSeek
- **Routing Mechanism**: Auto switch to backup provider when primary service fails
- **Client**: Expose unified chat and embedding interfaces

### 3. Intelligent Agent

- Manage dialogue context and memory
- Control tool invocation loops to avoid infinite execution
- Two working modes: Build (full features) / Plan (read-only)
- Stream tokens, thinking logs and tool call events in real time

### 4. Tool System (Core Highlight)

- **Auto Discovery**: Load all tools automatically by scanning the `tools/` directory
- **Decorator Registration**: Register functions as AI tools via `@tool`
- **Auto Schema Generation**: Generate LLM tool descriptions from function signatures and docstrings
- **File System Tools**: Read / Write / Append / Delete / Directory traversal
- **Repository Tools**: Generate project structure, code map, repository backup
- **Search Tools**: Search by filename, content and code symbols
- **System Tools**: Execute shell commands

### 5. RAG Cross-Session Memory (Core Highlight)

- Auto generate text embedding vectors when saving sessions
- Match historical sessions via cosine similarity
- Inject retrieved context into prompts automatically
- Zero extra dependency: Use official LLM embedding APIs, no local vector database required

### 6. Session Management

- Store sessions in local JSON files: `~/.minicode/sessions/`
- Support CRUD, keyword search and semantic search
- Auto generate session titles and timestamps

---

## IV. Core Frontend Modules

### 1. Layout System

- 3-column adaptive layout: Sidebar (File Tree) + Editor + Chat Panel
- Drag-to-resize, fullscreen toggle, collapse/expand panels
- Dark theme with optimized code syntax highlighting

### 2. Core Components

- **Sidebar**: Folder selection & file tree rendering
- **Editor**: Monaco editor for code editing and diff comparison
- **Chat**: Streaming chat, Markdown rendering, one-click code copy
- **SessionPanel**: History session management & semantic search
- **InputBox**: Toggle modes with Tab, send messages with Enter

### 3. State Management

- Reactive states: Working mode, active file, code content, diff data, panel status
- Encapsulated actions: Mode switch, file selection, diff update

### 4. API Communication

- Streaming chat: Receive tokens and tool events via SSE
- Session API: Timeout control to prevent hanging requests
- Proxy: Frontend forwards requests to backend port 8000 via `/api`

---

## V. Core Technical Advantages

- **Zero Deployment Cost**: No database or local models needed, one-click startup
- **Dual-mode Security**: Read-only Plan mode prevents misoperation; Build mode for full capabilities
- **Automatic LLM Failover**: Switch providers automatically when service fails
- **Rich Tool Ecosystem**: 20+ out-of-the-box programming tools, easy to extend
- **Cross-session Memory**: RAG retrieves history context automatically
- **Fully Local**: All data stays on local devices for privacy protection

---

## VI. Quick Start

### 1. Environment Requirements

- Python 3.10+
- Node.js 20+
- Valid API keys for LLM service providers

### 2. Start Backend

```bash
cd backend
python -m venv .venv
# Activate virtual environment
pip install -e .
# Create .env file and configure API keys
```

### 3. Start Frontend

```bash
cd frontend/vue
npm install
```

### 4. One-click Launch

```bash
minicode
```

Backend (Port 8000) and Frontend (Port 5173) will start automatically. Open browser to access.

---

## VII. Extension Development

### 1. Add New AI Tools

1. Create a new module under `tools/`
2. Register function with `@tool` decorator
3. Complete function signature and docstring (for auto schema generation)
4. Restart service to take effect

### 2. Add New LLM Provider

1. Inherit `BaseProvider` and implement generation & embedding methods
2. Register provider in `main.py`
3. Add corresponding API key and endpoint in config

### 3. Customize Frontend

- Modify `App.vue` for layout adjustment
- Extend `Chat.vue` to add new features
- Customize theme styles

---

## VIII. Design Philosophy

- **Minimalism**: Less dependencies, simpler configuration, lower learning cost
- **Local-first**: Data localization, privacy as priority
- **Tool-driven**: Focus on programming assistance rather than pure chat
- **Extensibility**: Modular design for easy expansion of tools, LLMs and frontend
- **Practicality**: Solve real programming problems instead of fancy features

---

## License

MIT
