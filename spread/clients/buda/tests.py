from django.test import AsyncTestCase
from aioresponses import aioresponses
from .client import BudaAPIClient, BudaAPIEndpoint


class BudaAPIClientTestBase(AsyncTestCase):
    async def setUp(self):
        self.client = BudaAPIClient()
        self.mock_aiohttp = aioresponses()
        self.mock_aiohttp.start()

    async def tearDown(self):
        self.mock_aiohttp.stop()
        await self.client.close()


class TestGetMarkets(BudaAPIClientTestBase):
    async def test_get_markets(self):
        mock_data = {
            "markets": [
                {
                    "id": "market1",
                    "name": "Market 1",
                    "base_currency": "BTC",
                    "quote_currency": "USD",
                    "minimum_order_amount": ["1.0", "BTC"],
                    "taker_fee": "0.01",
                    "maker_fee": "0.01",
                    "max_orders_per_minute": "10",
                    "maker_discount_percentage": "0.5",
                    "taker_discount_percentage": "0.5",
                    "disabled": False,
                }
            ]
        }
        self.mock_aiohttp.get(
            f"{self.client.base_url}{BudaAPIEndpoint.MARKETS.value}", payload=mock_data
        )

        markets = await self.client.get_markets()

        self.assertEqual(len(markets), 1)
        self.assertEqual(markets[0].id, "market1")
        self.assertEqual(markets[0].name, "Market 1")
        self.assertEqual(markets[0].minimum_order_amount.amount, 1.0)


class TestGetOrderBook(BudaAPIClientTestBase):
    async def test_get_order_book(self):
        market_id = "market1"
        mock_data = {
            "order_book": {
                "asks": [["100.0", "1.0"], ["101.0", "2.0"]],
                "bids": [["99.0", "1.5"], ["98.0", "2.5"]],
            }
        }
        self.mock_aiohttp.get(
            f"{self.client.base_url}{BudaAPIEndpoint.ORDER_BOOK.value.format(market_id=market_id)}",
            payload=mock_data,
        )

        order_book = await self.client.get_order_book(market_id)

        self.assertEqual(len(order_book.asks), 2)
        self.assertEqual(order_book.asks[0].price, 100.0)
        self.assertEqual(order_book.asks[0].amount, 1.0)


class TestGetTicker(BudaAPIClientTestBase):
    async def test_get_ticker(self):
        market_id = "market1"
        mock_data = {
            "ticker": {
                "market_id": market_id,
                "last_price": ["100.0", "USD"],
                "min_ask": ["101.0", "USD"],
                "max_bid": ["99.0", "USD"],
                "volume": ["500.0", "BTC"],
                "price_variation_24h": "0.05",
                "price_variation_7d": "0.1",
            }
        }
        self.mock_aiohttp.get(
            f"{self.client.base_url}{BudaAPIEndpoint.TICKER.value.format(market_id=market_id)}",
            payload=mock_data,
        )

        ticker = await self.client.get_ticker(market_id)

        self.assertEqual(ticker.market_id, market_id)
        self.assertEqual(ticker.last_price.amount, 100.0)
        self.assertEqual(ticker.min_ask.amount, 101.0)
        self.assertEqual(ticker.max_bid.amount, 99.0)


class TestGetMarket(BudaAPIClientTestBase):
    async def test_get_market(self):
        market_id = "market1"
        mock_data = {
            "market": {
                "id": market_id,
                "name": "Market 1",
                "base_currency": "BTC",
                "quote_currency": "USD",
                "minimum_order_amount": ["1.0", "BTC"],
                "taker_fee": "0.01",
                "maker_fee": "0.01",
                "max_orders_per_minute": "10",
                "maker_discount_percentage": "0.5",
                "taker_discount_percentage": "0.5",
                "disabled": False,
            }
        }
        self.mock_aiohttp.get(
            f"{self.client.base_url}{BudaAPIEndpoint.MARKET.value.format(market_id=market_id)}",
            payload=mock_data,
        )

        market = await self.client.get_market(market_id)

        self.assertEqual(market.id, market_id)
        self.assertEqual(market.name, "Market 1")
