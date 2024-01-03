from __future__ import annotations
from typing import Self
from enum import Enum
from dataclasses import dataclass

from spread.clients.buda.types import Ticker


class SpreadAlertStatus(str, Enum):
    GREATER = "GRATER"
    SMALLER = "SMALLER"
    EQUAL = "EQUAL"

    @classmethod
    def from_difference(cls, spread, threshold) -> Self:
        if spread > threshold:
            return cls.GREATER
        if spread < threshold:
            return cls.SMALLER
        return cls.EQUAL


@dataclass
class SpreadAlertTracking:
    alert_id: str
    market_id: str
    threshold: float
    spread: float
    status: SpreadAlertStatus


@dataclass
class MarketSpread:
    market_id: str
    spread_amount: float

    @classmethod
    def from_ticker(cls, ticker: Ticker) -> Self:
        min_ask_price = ticker.min_ask.amount
        max_bid_price = ticker.max_bid.amount
        spread_amount = min_ask_price - max_bid_price
        if spread_amount <= 0:
            spread_amount = 0
        return cls(ticker.market_id, spread_amount)
