from minicode.llm.providers.base import BaseProvider
from minicode import config


class DeepSeekProvider(BaseProvider):
    def __init__(
        self,
        api_key: str = config.DEEPSEEK_API_KEY,
        model: str = config.DEEPSEEK_MODEL,
        endpoint: str = config.DEEPSEEK_ENDPOINT,
        timeout: int = 60,
    ):
        super().__init__(api_key, model, endpoint, timeout)

    def _normalize_tool_calls(self, delta) -> list:
        raw = delta.get("tool_calls", [])
        result = []
        for i, tc in enumerate(raw):
            if i > 0:
                break
            func = tc.get("function", {})
            result.append(
                {
                    "name": func.get("name", ""),
                    "arguments": func.get("arguments", ""),
                }
            )
        return result
