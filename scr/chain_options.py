from typing import Optional
from scr.transforms import transform
from scr.selenium import selenium_options
from scr.scr_option import ScrOption
from scr import chain, context


class ChainOptions:
    default_text_encoding: ScrOption[str]
    prefer_parent_text_encoding: ScrOption[bool]
    force_text_encoding: ScrOption[bool]

    selenium_variant: ScrOption[selenium_options.SeleniumVariant]
    selenium_page_acceptance: ScrOption[selenium_options.SeleniumPageAcceptance]
    selenium_download_strategy: ScrOption[selenium_options.SeleniumDownloadStrategy]

    subchains: list['ChainOptions']
    transforms: list[transform.Transform]

    def __init__(
        self,
        default_text_encoding: Optional[str] = None,
        prefer_parent_text_encoding: Optional[bool] = None,
        force_text_encoding: Optional[bool] = None,

        selenium_variant: Optional[selenium_options.SeleniumVariant] = None,
        selenium_page_acceptance: Optional[selenium_options.SeleniumPageAcceptance] = None,
        selenium_download_strategy: Optional[selenium_options.SeleniumDownloadStrategy] = None,

        subchains: Optional[list['ChainOptions']] = None,
        transforms: Optional[list[transform.Transform]] = None,
    ) -> None:
        self.default_text_encoding = ScrOption(default_text_encoding)
        self.prefer_parent_text_encoding = ScrOption(prefer_parent_text_encoding)
        self.force_text_encoding = ScrOption(force_text_encoding)
        self.selenium_variant = ScrOption(selenium_variant)
        self.selenium_page_acceptance = ScrOption(selenium_page_acceptance)
        self.selenium_download_strategy = ScrOption(selenium_download_strategy)
        self.subchains = subchains if subchains is not None else []
        self.transforms = transforms if transforms is not None else []


def create_chain(chain: ChainOptions, ctx: 'context.Context') -> 'chain.Chain':
    raise NotImplementedError


def update_root_chain(chain: ChainOptions, prev: 'chain.Chain') -> 'chain.Chain':
    raise NotImplementedError


DEFAULT_CHAIN_OPTIONS = ChainOptions(
    default_text_encoding="utf-8",
    prefer_parent_text_encoding=False,
    force_text_encoding=False,
    selenium_variant=selenium_options.SeleniumVariant.DISABLED,
    selenium_page_acceptance=selenium_options.SeleniumPageAcceptance.PLAIN,
    selenium_download_strategy=selenium_options.SeleniumDownloadStrategy.SCR
)
