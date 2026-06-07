from minicode import config
from minicode.llm.providers.qwen import QwenProvider
from minicode.llm.providers.glm import GLMProvider
from minicode.llm.providers.deepseek import DeepSeekProvider


class ModelRouter:
    def __init__(
        self,
        providers: dict[str, QwenProvider | GLMProvider | DeepSeekProvider],
        primary=config.PRIMARY_PROVIDER,
        fallback=config.FALLBACK_PROVIDER,
    ):
        self.providers = providers
        self.primary = primary
        self.fallback = fallback

    def get_primary(self) -> QwenProvider | GLMProvider | DeepSeekProvider:
        return self.providers[self.primary]

    def get_fallback(self) -> QwenProvider | GLMProvider | DeepSeekProvider:
        return self.providers[self.fallback]
