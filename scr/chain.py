from scr import context, chain, chain_prototype
from scr.selenium import selenium_context, selenium_options
from scr.transforms import transform, transform_ref
from typing import Optional, cast


class Chain(chain_prototype.ChainPrototype):
    ctx: 'context.Context'
    parent: Optional['Chain']
    default_text_encoding: str
    prefer_parent_text_encoding: bool
    force_text_encoding: bool

    selenium_ctx: Optional['selenium_context.SeleniumContext']
    selenium_download_strategy: 'selenium_options.SeleniumDownloadStrategy'

    transforms: list['transform.Transform']

    subchains: list['chain.Chain']

    aggregation_targets: list['transform_ref.TransformRef']

    def __init__(
        self,
        ctx: 'context.Context',
        parent: Optional['Chain'],
        default_text_encoding: str,
        prefer_parent_text_encoding: bool,
        force_text_encoding: bool,

        selenium_ctx: Optional['selenium_context.SeleniumContext'],
        selenium_download_strategy: 'selenium_options.SeleniumDownloadStrategy',

        transforms: list['transform.Transform'],
    ) -> None:
        self.ctx = ctx
        self.parent = parent
        self.default_text_encoding = default_text_encoding
        self.prefer_parent_text_encoding = prefer_parent_text_encoding
        self.force_text_encoding = force_text_encoding
        self.selenium_ctx = selenium_ctx
        self.selenium_download_strategy = selenium_download_strategy
        self.transforms = transforms
        self.aggregation_targets = []

    def set_subchains(self, subchains: list['Chain']) -> None:
        self.subchains = subchains

    def root(self) -> 'Chain':
        return cast(Chain, super().root())

    def setup(self) -> None:
        for i in range(0, len(self.transforms)):
            self.transforms[i] = self.transforms[i].setup(self, i)
