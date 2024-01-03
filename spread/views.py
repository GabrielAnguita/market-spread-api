from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action

from .services.markets import get_market
from .services.markets import ObjectDoesNotExist
from .services.markets import get_markets
from .services.spread import get_market_spread
from .services.spread import get_all_spreads
from .services.spread_alert import get_alert_status

from .serializers import MarketSerializer
from .serializers import MarketSpreadDataSerializer
from .serializers import SpreadAlertTrackingSerializer
from .serializers import SpreadAlertSerializer

from .models import SpreadAlert

from drf_spectacular.utils import extend_schema_view
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiParameter


class MarketViewSet(ViewSet):
    serializer_class = MarketSerializer

    def list(self, request, *args, **kwargs):
        markets = get_markets()
        data = [self.serializer_class(instance=market).data for market in markets]
        return Response(data)

    @extend_schema(
        parameters=[
            OpenApiParameter(name="id", type=str, location=OpenApiParameter.PATH)
        ],
    )
    def retrieve(self, request, pk=None):
        try:
            spread = get_market(pk)
        except ObjectDoesNotExist:
            return Response(status=404)
        serializer = self.serializer_class(instance=spread)
        return Response(serializer.data)

    @extend_schema(
        responses=MarketSpreadDataSerializer(many=True),
    )
    @action(methods=["GET"], detail=False, url_path="spreads")
    def all_spreads(self, request):
        spreads = get_all_spreads()
        serializer = MarketSpreadDataSerializer(instance=spreads, many=True)
        return Response(serializer.data)

    @extend_schema(
        responses={200: MarketSpreadDataSerializer},
        parameters=[
            OpenApiParameter(name="id", type=str, location=OpenApiParameter.PATH)
        ],
    )
    @action(methods=["GET"], detail=True, url_path="spread")
    def spread(self, request, pk=None):
        spread = get_market_spread(pk)
        serializer = MarketSpreadDataSerializer(instance=spread)
        return Response(serializer.data)


@extend_schema_view(retrieve=extend_schema(responses=SpreadAlertTrackingSerializer))
class SpreadAlertViewSet(
    mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet
):
    queryset = SpreadAlert.objects.all()
    serializer_class = SpreadAlertSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        status = get_alert_status(instance)
        serializer = SpreadAlertTrackingSerializer(instance=status)
        return Response(serializer.data)
