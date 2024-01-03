from unittest.mock import AsyncMock
from unittest.mock import patch, MagicMock

from django.test import TestCase

from spread.clients.buda import BudaAPIClient
from spread.clients.buda.types import Market
from spread.clients.buda.types import Ticker
from spread.services.markets import get_market
from spread.services.markets import get_markets
from spread.services.markets import market_exists
from spread.services.markets import ObjectDoesNotExist
from spread.services.spread import get_all_spreads
from spread.services.spread import get_market_spread
from spread.services.types import MarketSpread

from aiohttp.client_exceptions import ClientResponseError


class MarketServicesTestCase(TestCase):
    def test_get_markets(self):
        expected = [
            Market(
                **{
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
            ),
            Market(
                **{
                    "id": "market2",
                    "name": "Market 2",
                    "base_currency": "BTC",
                    "quote_currency": "LOL",
                    "minimum_order_amount": ["1.0", "BTC"],
                    "taker_fee": "0.01",
                    "maker_fee": "0.01",
                    "max_orders_per_minute": "10",
                    "maker_discount_percentage": "0.5",
                    "taker_discount_percentage": "0.5",
                    "disabled": False,
                }
            ),
        ]
        mock_func = AsyncMock()
        mock_func.return_value = expected

        with patch.object(BudaAPIClient, "get_markets", mock_func):
            markets = get_markets()

            self.assertEqual(markets, expected)

    def test_get_market(self):
        expected = Market(
            **{
                "id": "market_id",
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
        )
        mock_func = AsyncMock()
        mock_func.return_value = expected

        with patch.object(BudaAPIClient, "get_market", mock_func):
            market = get_market("market_id")

            self.assertEqual(market, expected)

    @patch("spread.services.markets.BudaAPIClient")
    def test_get_market_not_found(self, mock_client):
        mock_client.return_value.get_market.side_effect = ClientResponseError(
            None, None, status=404
        )

        with self.assertRaises(ObjectDoesNotExist):
            get_market("market_id")

    @patch("spread.services.markets.get_market")
    def test_market_exists(self, mock_get_market):
        exists = market_exists("market_id")

        self.assertTrue(exists)

    @patch("spread.services.markets.get_market")
    def test_market_does_not_exist(self, mock_get_market):
        mock_get_market.side_effect = ObjectDoesNotExist

        exists = market_exists("market_id")

        self.assertFalse(exists)


class MarketSpreadTestCase(TestCase):
    def test_get_zero_spread(self):
        max_bid_amount = 879658.0
        min_ask_amount = 876531.11
        mock_ticker = Ticker.from_response(
            {
                "last_price": ["879789.0", "CLP"],
                "market_id": "BTC-CLP",
                "max_bid": [str(max_bid_amount), "CLP"],
                "min_ask": [str(min_ask_amount), "CLP"],
                "price_variation_24h": "0.005",
                "price_variation_7d": "0.1",
                "volume": ["102.0", "BTC"],
            }
        )
        mock_get_ticker = AsyncMock()
        mock_get_ticker.return_value = mock_ticker

        with patch.object(BudaAPIClient, "get_ticker", mock_get_ticker):
            market_spread = get_market_spread("market_id")

        self.assertIsInstance(market_spread, MarketSpread)
        self.assertEqual(market_spread.spread_amount, 0)

    def test_get_nonzero_spread(self):
        max_bid_amount = 876531.11
        min_ask_amount = 879658.0
        mock_ticker = Ticker.from_response(
            {
                "last_price": ["879789.0", "CLP"],
                "market_id": "BTC-CLP",
                "max_bid": [str(max_bid_amount), "CLP"],
                "min_ask": [str(min_ask_amount), "CLP"],
                "price_variation_24h": "0.005",
                "price_variation_7d": "0.1",
                "volume": ["102.0", "BTC"],
            }
        )
        mock_get_ticker = AsyncMock()
        mock_get_ticker.return_value = mock_ticker

        with patch.object(BudaAPIClient, "get_ticker", mock_get_ticker):
            market_spread = get_market_spread("market_id")

        self.assertIsInstance(market_spread, MarketSpread)
        self.assertEqual(market_spread.spread_amount, min_ask_amount - max_bid_amount)
        self.assertTrue(market_spread.spread_amount > 0)

    def test_get_all_spreads(self):
        mock_markets = [
            Market(
                **{
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
            ),
            Market(
                **{
                    "id": "market2",
                    "name": "Market 2",
                    "base_currency": "BTC",
                    "quote_currency": "LOL",
                    "minimum_order_amount": ["1.0", "BTC"],
                    "taker_fee": "0.01",
                    "maker_fee": "0.01",
                    "max_orders_per_minute": "10",
                    "maker_discount_percentage": "0.5",
                    "taker_discount_percentage": "0.5",
                    "disabled": False,
                }
            ),
        ]
        mock_tickers = [
            Ticker.from_response(
                {
                    "last_price": ["879789.0", "CLP"],
                    "market_id": "BTC-CLP",
                    "max_bid": ["879789.0", "CLP"],
                    "min_ask": ["890789.0", "CLP"],
                    "price_variation_24h": "0.005",
                    "price_variation_7d": "0.1",
                    "volume": ["102.0", "BTC"],
                }
            ),
            Ticker.from_response(
                {
                    "last_price": ["879789.0", "CLP"],
                    "market_id": "BTC-CLP",
                    "max_bid": ["879789.0", "CLP"],
                    "min_ask": ["890789.0", "CLP"],
                    "price_variation_24h": "0.005",
                    "price_variation_7d": "0.1",
                    "volume": ["102.0", "BTC"],
                }
            ),
        ]
        mock_get_ticker = AsyncMock()
        mock_get_ticker.side_effect = mock_tickers
        mock_get_markets = AsyncMock()
        mock_get_markets.return_value = mock_markets

        with patch.object(BudaAPIClient, "get_ticker", mock_get_ticker), patch.object(
            BudaAPIClient, "get_markets", mock_get_markets
        ):
            all_spreads = get_all_spreads()

        self.assertEqual(len(all_spreads), 2)
        self.assertIsInstance(all_spreads[0], MarketSpread)
        self.assertIsInstance(all_spreads[1], MarketSpread)
