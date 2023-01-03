from typing import Optional
from scr.transforms import transform
from scr import match, chain
import re


class Regex(transform.Transform):
    regex: re.Pattern[str]

    @staticmethod
    def name_matches(name: str) -> bool:
        return "regex".startswith(name)

    def __init__(self, name: str, label: Optional[str], regex: str) -> None:
        super().__init__(label if label is not None else name)
        try:
            self.regex = re.compile(regex, re.DOTALL | re.MULTILINE)
        except re.error as err:
            raise ValueError(f"invalid regex: {err.msg}")

    def apply_single(self, c: chain.Chain, m: match.Match, res: list[match.Match]) -> None:
        m = m.resolve()
        if not isinstance(m, match.MatchText):
            raise ValueError("the regex transform only works on text")

        for re_match in self.regex.finditer(m.text):
            text = re_match.group(0)
            mres = match.MatchText(m, text if text is not None else "")
            for k, v in re_match.groupdict().items():
                mres.args[k] = match.MatchText(m, v if v is not None else "")
            for i, g in enumerate(re_match.groups()):
                mres.args[self.label + str(i)] = match.MatchText(m, g if g is not None else "")
            res.append(mres)
