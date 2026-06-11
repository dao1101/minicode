from minicode import config
from minicode.llm.providers.base import BaseProvider


class ModelRouter:
    def __init__(
        self,
        providers: dict[str, BaseProvider],
        primary=config.PRIMARY_PROVIDER,
        fallback=config.FALLBACK_PROVIDER,
    ):
        self.providers = providers
        self.primary = primary
        self.fallback = fallback

    def get_primary(self) -> BaseProvider:
        return self.providers[self.primary]

    def get_fallback(self) -> BaseProvider:
        return self.providers[self.fallback]

    def get_embed(self) -> BaseProvider:
        return self.providers[config.EMBEDDING_PROVIDER]
