from __future__ import annotations

import re
from dataclasses import dataclass

_PRICE_PATTERN = re.compile(r'(?<!\w)\$?\s*(\d{1,3}(?:,\d{3})*(?:\.\d+)?|\d+(?:\.\d+)?)')
_FIRM_ALIASES: dict[str, tuple[str, ...]] = {
    'FTMO': ('ftmo',),
    'Topstep': ('topstep',),
    'Apex Trader Funding': ('apex', 'apex trader funding'),
    'FundedNext': ('fundednext', 'funded next'),
    'MyFundedFutures': ('myfundedfutures', 'my funded futures'),
}


@dataclass(frozen=True)
class ParsedPasteOrder:
    raw_text: str
    price: float | None
    prop_firm: str | None


def parse_price(text: str) -> float | None:
    for match in _PRICE_PATTERN.finditer(text):
        token = match.group(1).replace(',', '')
        try:
            value = float(token)
        except ValueError:
            continue
        if value > 0:
            return value
    return None


def detect_prop_firm(text: str) -> str | None:
    lowered = text.lower()
    for canonical, aliases in _FIRM_ALIASES.items():
        if any(alias in lowered for alias in aliases):
            return canonical
    return None


def parse_paste_order(text: str) -> ParsedPasteOrder:
    return ParsedPasteOrder(raw_text=text, price=parse_price(text), prop_firm=detect_prop_firm(text))
