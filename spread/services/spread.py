import asyncio

from spread.clients.buda import BudaAPIClient
from .types import MarketSpread


def get_market_spread(market_id: str) -> MarketSpread:
    client = BudaAPIClient()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        ticker = loop.run_until_complete(client.get_ticker(market_id))
        loop.run_until_complete(client.close())
    finally:
        loop.close()
    return MarketSpread.from_ticker(ticker)


def get_all_spreads() -> list[MarketSpread]:
    client = BudaAPIClient()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        markets = loop.run_until_complete(client.get_markets())
        tasks = [client.get_ticker(market.id) for market in markets]
        tickers = loop.run_until_complete(asyncio.gather(*tasks))
        loop.run_until_complete(client.close())
    finally:
        loop.close()
    return [MarketSpread.from_ticker(ticker) for ticker in tickers]
