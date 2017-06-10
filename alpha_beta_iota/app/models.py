from django.db import models
from ulid2 import generate_ulid_as_uuid

# class User(models.Model):
#    id = models.UUIDField(default=generate_ulid_as_uuid, primary_key=True)

class AssetType:
    CASH = 'cash'
    STOCKS = 'stocks'
    CANADIAN = 'canadian'
    OTC = 'otc'
    FOREX = 'forex'
    FUTURES = 'futures'
    INDEXES = 'indexes'

# class AssetTick(models.Model):

class AssetTickSummary(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=12, null=False, default=AssetType.STOCKS)
    sym = models.CharField(max_length=12, null=False)
    dt = models.DateTimeField(null=False)
    o = models.BigIntegerField(null=False)
    h = models.BigIntegerField(null=False)
    l = models.BigIntegerField(null=False)
    c = models.BigIntegerField(null=False)
    vol = models.BigIntegerField(null=False)

    class Meta:
        indexes = [
            models.Index(fields=['type', 'sym', 'dt'], name='asset_tick_summary_comp_idx'),
            models.Index(fields=['type'], name='asset_tick_summary_type_idx'),
            models.Index(fields=['sym'], name='asset_tick_summary_sym_idx'),
            models.Index(fields=['dt'], name='asset_tick_summary_dt_idx'),
        ]
