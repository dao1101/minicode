from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Any

from minicode import config

from minicode.core.agent import Agent
from minicode.core.controller import Controller

from minicode.llm.client import ModelClient
from minicode.llm.router import ModelRouter
from minicode.llm.providers.base import BaseProvider
from minicode.llm.providers.glm import GLMProvider
from minicode.llm.providers.qwen import QwenProvider
from minicode.llm.providers.deepseek import DeepSeekProvider

from minicode.memory.context import Context

from minicode.plan.planner import PlanGenerator
from minicode.plan.builder import Builder

from minicode.runtime.step_controller import StepController

from minicode.tools.loader import load_tools
from minicode.tools.registry import get_registry
from minicode.tools.runner import ToolRunner

from minicode.sessions import save_session, list_sessions, get_session, delete_session

import json


def _create_controller():
    load_tools()

    providers: dict[str, BaseProvider] = {
        "qwen": QwenProvider(
            api_key=config.QWEN_API_KEY,
            model=config.QWEN_MODEL,
            endpoint=config.QWEN_ENDPOINT,
        ),
        "glm": GLMProvider(
            api_key=config.GLM_API_KEY,
            model=config.GLM_MODEL,
            endpoint=config.GLM_ENDPOINT,
        ),
        "deepseek": DeepSeekProvider(
            api_key=config.DEEPSEEK_API_KEY,
            model=config.DEEPSEEK_MODEL,
            endpoint=config.DEEPSEEK_ENDPOINT,
        ),
    }

    router = ModelRouter(
        providers=providers,
        primary=config.PRIMARY_PROVIDER,
        fallback=config.FALLBACK_PROVIDER,
    )

    llm = ModelClient(router)

    memory = Context()
    registry = get_registry()
    runner = ToolRunner(registry)
    step_controller = StepController(config.MAX_STEP)

    agent = Agent(
        llm=llm,
        memory=memory,
        registry=registry,
        runner=runner,
        step_controller=step_controller,
    )

    planner = PlanGenerator(llm, registry)
    plan_builder = Builder(runner)

    controller = Controller(agent, planner, plan_builder)

    return controller


api = FastAPI(title="MiniCode API")

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

controller = _create_controller()


@api.get("/")
async def root():
    return {"message": "MiniCode API is running", "version": "1.0.0"}


@api.post("/chat")
async def chat(req: Request):
    data = await req.json()
    message = data.get("message", "")
    mode = data.get("mode", "build")
    if mode not in ("build", "plan"):
        mode = "build"

    if not message.strip():
        return JSONResponse({"error": "Empty message"}, status_code=400)

    def _event_stream():
        for event in controller.chat_stream(message, mode):
            yield f"data: {json.dumps(event, ensure_ascii=False)}\n\n"

    return StreamingResponse(_event_stream(), media_type="text/event-stream")


@api.get("/ping")
async def ping():
    return {"status": "ok"}


# ─── Sessions ────────────────────────────────────────────────────────────────


class SaveSessionRequest(BaseModel):
    title: str = ""
    messages: List[Any]


@api.get("/sessions")
async def sessions_list(q: str = ""):
    return list_sessions(query=q)


@api.post("/sessions")
async def sessions_save(body: SaveSessionRequest):
    meta = save_session(body.title, body.messages)
    return meta


@api.get("/sessions/{session_id}")
async def sessions_get(session_id: str):
    data = get_session(session_id)
    if data is None:
        return JSONResponse({"error": "not found"}, status_code=404)
    return data


@api.delete("/sessions/{session_id}")
async def sessions_delete(session_id: str):
    ok = delete_session(session_id)
    return {"ok": ok}


# ─── Entry point ─────────────────────────────────────────────────────────────


def main():
    import subprocess
    import os
    import shutil

    provider_key_map = {
        "qwen": ("QWEN_API_KEY", config.QWEN_API_KEY),
        "glm": ("GLM_API_KEY", config.GLM_API_KEY),
        "deepseek": ("DEEPSEEK_API_KEY", config.DEEPSEEK_API_KEY),
    }
    primary_key_name, primary_key = provider_key_map.get(
        config.PRIMARY_PROVIDER, ("", "")
    )
    if not primary_key:
        print(
            f"[MiniCode] Warning: {primary_key_name or 'PRIMARY_PROVIDER'} is not set"
        )

    if config.QWEN_API_KEY:
        print(f"[MiniCode] QWEN endpoint: {config.QWEN_ENDPOINT}")
    if config.GLM_API_KEY:
        print(f"[MiniCode] GLM endpoint: {config.GLM_ENDPOINT}")
    if config.DEEPSEEK_API_KEY:
        print(f"[MiniCode] DeepSeek endpoint: {config.DEEPSEEK_ENDPOINT}")

    vue_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..", "frontend", "vue")
    )

    frontend_proc = None
    npm_path = shutil.which("npm")
    if npm_path and os.path.isdir(os.path.join(vue_dir, "node_modules")):
        frontend_proc = subprocess.Popen(
            [npm_path, "run", "dev"],
            cwd=vue_dir,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            shell=False,
        )
        print(f"[MiniCode] Frontend starting at http://localhost:5173")

        import threading

        def _open_browser():
            import time, webbrowser

            time.sleep(3)
            webbrowser.open("http://localhost:5173")

        threading.Thread(target=_open_browser, daemon=True).start()
    else:
        missing = []
        if not npm_path:
            missing.append("npm not found in PATH")
        if not os.path.isdir(os.path.join(vue_dir, "node_modules")):
            missing.append("node_modules missing (run npm install)")
        print(f"[MiniCode] Frontend not started: {', '.join(missing)}")

    import uvicorn

    try:
        uvicorn.run(api, host="0.0.0.0", port=8000, reload=False)
    finally:
        if frontend_proc:
            frontend_proc.terminate()
            frontend_proc.wait()


if __name__ == "__main__":
    main()
