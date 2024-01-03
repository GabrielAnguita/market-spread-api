from enum import Enum
from functools import cached_property

import aiohttp

from .types import OrderBook
from .types import Market
from .types import Ticker

from django.conf import settings


class BudaAPIEndpoint(str, Enum):
    MARKETS = "markets"
    MARKET = "markets/{market_id:s}"
    ORDER_BOOK = "markets/{market_id:s}/order_book"
    TICKER = "markets/{market_id:s}/ticker"
    TICKERS = "tickers"


class BudaAPIClient:
    def __init__(self):
        self.base_url = settings.BUDA_API_BASE_URL

    @cached_property
    def async_session(self):
        return aiohttp.ClientSession()

    async def get(
        self,
        endpoint: BudaAPIEndpoint,
        **path_params,
    ) -> dict:
        return await self.make_request("GET", endpoint, path_params)

    async def make_request(
        self,
        method: str,
        endpoint: BudaAPIEndpoint,
        path_params: dict,
    ) -> dict:
        url = self.build_url(endpoint, path_params)
        async with self.async_session.request(method, url) as response:
            response.raise_for_status()
            return await response.json()

    def build_url(
        self,
        path: BudaAPIEndpoint,
        path_params: dict[str, str] | None = None,
    ) -> str:
        path_params = path_params or {}
        return self.base_url + path.value.format(**path_params)

    async def get_markets(self) -> list[Market]:
        data = await self.get(BudaAPIEndpoint.MARKETS)
        return [Market.from_response(market_data) for market_data in data["markets"]]

    async def get_order_book(self, market_id: str) -> OrderBook:
        order_book_data = await self.get(
            BudaAPIEndpoint.ORDER_BOOK, market_id=market_id
        )
        return OrderBook.from_response(order_book_data)

    async def get_ticker(self, market_id: str) -> Ticker:
        ticker_data = await self.get(BudaAPIEndpoint.TICKER, market_id=market_id)
        return Ticker.from_response(ticker_data["ticker"])

    async def get_market(self, market_id: str) -> Market:
        data = await self.get(BudaAPIEndpoint.MARKET, market_id=market_id)
        return Market.from_response(data["market"])

    async def close(self) -> None:
        await self.async_session.close()
