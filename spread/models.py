from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator


class SpreadAlert(models.Model):
    market_id = models.TextField()
    alert_threshold = models.FloatField(validators=[MinValueValidator(0.0)])

    class Meta:
        verbose_name = _("spread alert")
        verbose_name_plural = _("spread alerts")
