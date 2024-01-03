from spread.services.types import MarketSpread
from spread.services.types import SpreadAlertTracking

from spread.models import SpreadAlert

from rest_framework_dataclasses.serializers import DataclassSerializer
from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError

from spread.services.markets import market_exists

from spread.clients.buda.types import Market


class MarketSerializer(DataclassSerializer):
    class Meta:
        dataclass = Market


class MarketSpreadDataSerializer(DataclassSerializer):
    class Meta:
        dataclass = MarketSpread


class SpreadAlertCreateSerializer(ModelSerializer):
    class Meta:
        model = SpreadAlert
        fields = ["market_id", "alert_threshold"]

    def validate_market_id(self, market_id):
        if not market_exists(market_id):
            msg = "Cannot track spread for non-existing market"
            raise ValidationError(msg)


class SpreadAlertSerializer(ModelSerializer):
    class Meta:
        model = SpreadAlert
        fields = ["id", "market_id", "alert_threshold"]

    def validate_market_id(self, market_id):
        if not market_exists(market_id):
            msg = "Cannot track spread for non-existing market"
            raise ValidationError(msg)
        return market_id


class SpreadAlertTrackingSerializer(DataclassSerializer):
    class Meta:
        dataclass = SpreadAlertTracking
