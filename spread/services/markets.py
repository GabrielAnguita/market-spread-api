from spread.clients.buda import BudaAPIClient
from spread.clients.buda.types import Market

import asyncio
from aiohttp.client_exceptions import ClientResponseError


class ObjectDoesNotExist(Exception):
    ...


def get_markets() -> list[Market]:
    client = BudaAPIClient()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        markets = loop.run_until_complete(client.get_markets())
        loop.run_until_complete(client.close())
    finally:
        loop.close()
    return markets


def get_market(market_id) -> Market:
    client = BudaAPIClient()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        market = loop.run_until_complete(client.get_market(market_id))
        loop.run_until_complete(client.close())
    except ClientResponseError as exc:
        if exc.status == 404:
            raise ObjectDoesNotExist from exc
    finally:
        loop.close()
    return market


def market_exists(market_id: str) -> bool:
    try:
        get_market(market_id)
    except ObjectDoesNotExist:
        return False
    return True
