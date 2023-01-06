from scr.transforms import transform
from scr import chain_spec, chain, chain_options, match, range_spec
from typing import Optional


class Split(transform.Transform):
    target: 'chain_spec.ChainSpec'

    @staticmethod
    def name_matches(name: str) -> bool:
        return "next".startswith(name)

    @staticmethod
    def create(label: str, value: Optional[str], chainspec: 'chain_spec.ChainSpec') -> 'transform.Transform':
        if value is None:
            return Split(label, chain_spec.ChainSpecSubrange(range_spec.RangeSpecBounds(None, None), chain_spec.ChainSpecCurrent()))
        try:
            return Split(label, chain_spec.parse_chain_spec(value))
        except chain_spec.ChainSpecParseException as ex:
            raise transform.TransformValueError(f"invalid range for 'next': {ex}")

    def __init__(self, label: str, target: 'chain_spec.ChainSpec') -> None:
        super().__init__(label)

    def apply(self, c: 'chain.Chain', m: 'match.Match') -> 'match.Match':
        return m

    def get_next_chain_context(self, current: 'chain_options.ChainOptions') -> 'chain_options.ChainOptions':
        res = None
        for tc in self.target.instantiate(current):
            assert res is None
            res = tc
        assert res is not None
        return res
