import requests
import json


class BaseProvider:
    def __init__(
        self,
        api_key: str,
        model: str,
        endpoint: str,
        timeout: int = 60,
    ):
        self.api_key = api_key
        self.model = model
        self.endpoint = endpoint
        self.timeout = timeout

    def _build_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _build_payload(self, messages, tools=None) -> dict:
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": True,
        }
        if tools:
            payload["tools"] = tools
        return payload

    def _normalize_tool_calls(self, delta) -> list:
        raise NotImplementedError

    def generate_stream(self, messages, tools=None):
        tool_buffer: dict = {}

        headers = self._build_headers()
        payload = self._build_payload(messages, tools)

        resp = requests.post(
            self.endpoint,
            headers=headers,
            json=payload,
            stream=True,
            timeout=self.timeout,
        )

        resp.raise_for_status()

        for line in resp.iter_lines():
            if not line:
                continue

            line = line.decode("utf-8")

            if not line.startswith("data:"):
                continue

            data_str = line[5:].strip()

            if data_str == "[DONE]":
                break

            try:
                data = json.loads(data_str)
            except Exception:
                continue

            choices = data.get("choices", [])
            if not choices:
                continue

            delta = choices[0].get("delta", {})

            if "content" in delta and delta["content"]:
                yield {"type": "text", "content": delta["content"]}

            tool_calls = self._normalize_tool_calls(delta)
            for tc in tool_calls:
                call_id = "tool_0"

                if call_id not in tool_buffer:
                    tool_buffer[call_id] = {"name": "", "arguments": ""}

                if tc.get("name"):
                    tool_buffer[call_id]["name"] = tc["name"]

                if tc.get("arguments"):
                    tool_buffer[call_id]["arguments"] += tc["arguments"]

                name = tool_buffer[call_id]["name"]
                args_str = tool_buffer[call_id]["arguments"]

                if name and args_str:
                    try:
                        parsed_args = json.loads(args_str)
                        yield {
                            "type": "tool_call",
                            "id": call_id,
                            "name": name,
                            "arguments": parsed_args,
                        }
                        del tool_buffer[call_id]
                    except json.JSONDecodeError:
                        pass
