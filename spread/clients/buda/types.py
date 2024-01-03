from __future__ import annotations

from dataclasses import dataclass
from dataclasses import fields
from typing import Self, Any


@dataclass
class Order:
    price: float
    amount: float


@dataclass
class MoneyAmount:
    amount: float
    currency: str

    def __post_init__(self):
        self.amount = float(self.amount)


@dataclass
class OrderBook:
    asks: list[Order]
    bids: list[Order]

    @classmethod
    def from_response(cls, data: dict[Any, Any]) -> Self:
        return cls(
            asks=[
                Order(float(price), float(amount))
                for price, amount in data["order_book"]["asks"]
            ],
            bids=[
                Order(float(price), float(amount))
                for price, amount in data["order_book"]["bids"]
            ],
        )


@dataclass
class Market:
    id: str
    name: str
    base_currency: str
    quote_currency: str
    minimum_order_amount: MoneyAmount
    taker_fee: str
    maker_fee: str
    max_orders_per_minute: str
    maker_discount_percentage: str
    taker_discount_percentage: str
    disabled: bool

    @classmethod
    def from_response(cls, response: dict[Any, Any]) -> Self:
        data = {k.name: response[k.name] for k in fields(cls)}
        data["minimum_order_amount"] = MoneyAmount(*data["minimum_order_amount"])
        return cls(**data)


@dataclass
class Ticker:
    market_id: str
    last_price: MoneyAmount
    min_ask: MoneyAmount
    max_bid: MoneyAmount
    volume: MoneyAmount
    price_variation_24h: float
    price_variation_7d: float

    @classmethod
    def from_response(cls, data: dict[Any, Any]) -> Self:
        return cls(
            market_id=data["market_id"],
            last_price=MoneyAmount(*data["last_price"]),
            min_ask=MoneyAmount(*data["min_ask"]),
            max_bid=MoneyAmount(*data["max_bid"]),
            volume=MoneyAmount(*data["volume"]),
            price_variation_24h=float(data["price_variation_24h"]),
            price_variation_7d=float(data["price_variation_7d"]),
        )
