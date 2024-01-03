from __future__ import annotations

from .spread import get_market_spread

from .types import SpreadAlertStatus
from .types import SpreadAlertTracking

from ..models import SpreadAlert


def get_alert_status(spread_alert: SpreadAlert) -> SpreadAlertTracking:
    market_spread = get_market_spread(spread_alert.market_id)
    status = SpreadAlertStatus.from_difference(
        market_spread.spread_amount,
        spread_alert.alert_threshold,
    )
    return SpreadAlertTracking(
        spread_alert.pk,
        spread_alert.market_id,
        spread_alert.alert_threshold,
        float(market_spread.spread_amount),
        status,
    )
