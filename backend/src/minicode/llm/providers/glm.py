from minicode.llm.providers.base import BaseProvider
from minicode import config


class GLMProvider(BaseProvider):
    def __init__(
        self,
        api_key: str = config.GLM_API_KEY,
        model: str = config.GLM_MODEL,
        endpoint: str = config.GLM_ENDPOINT,
        timeout: int = 60,
    ):
        super().__init__(api_key, model, endpoint, timeout)

    def _normalize_tool_calls(self, delta) -> list:
        raw = delta.get("tool_calls", [])
        result = []
        for i, tc in enumerate(raw):
            if i > 0:
                break
            result.append(
                {
                    "name": tc.get("name", ""),
                    "arguments": tc.get("arguments", ""),
                }
            )
        return result
