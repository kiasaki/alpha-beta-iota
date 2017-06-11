from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    players = models.ManyToManyField(
        User,
        through='GameMembership',
        through_fields=('game', 'user'),
    )
    created_at = models.DateTimeField(null=False, auto_now_add=True)
    updated_at = models.DateTimeField(null=False, auto_now=True)

class GameMembership(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_owner = models.BooleanField()

class Account(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=255)
    game = models.ForeignKey(Game, null=True)
    created_at = models.DateTimeField(null=False, auto_now_add=True)
    updated_at = models.DateTimeField(null=False, auto_now=True)

class AssetType:
    CASH = 'cash'
    STOCKS = 'stocks'
    CANADIAN = 'canadian'
    OTC = 'otc'
    FOREX = 'forex'
    FUTURES = 'futures'
    INDEXES = 'indexes'

ASSET_TYPE_CHOICES = (
    ('cash', 'Cash'),
    ('stocks', 'Stocks'),
    ('canadian', 'Canadian Stock'),
    ('otc', 'OTC'),
    ('forex', 'Forex'),
    ('futures', 'Futures'),
    ('indexes', 'Indexes'),
)

class OrderStatus:
    OPENED = 'opened'
    CLOSED = 'closed'
    CANCELLED = 'cancelled'

ORDER_STATUS_CHOICES = (
    ('opened', 'Opened'),
    ('closed', 'closed'),
    ('cancelled', 'cancelled'),
)

class Order(models.Model):
    account = models.ForeignKey(Account)
    source_type = models.CharField(max_length=12, null=False, choices=ASSET_TYPE_CHOICES)
    target_type = models.CharField(max_length=12, null=False, choices=ASSET_TYPE_CHOICES)
    source_sym = models.CharField(max_length=12, null=False)
    target_sym = models.CharField(max_length=12, null=False)
    status = models.CharField(max_length=12, null=False, default=OrderStatus.OPENED, choices=ORDER_STATUS_CHOICES)
    amount = models.BigIntegerField(null=False)
    price = models.BigIntegerField(null=False)
    dt = models.DateTimeField(null=False)
    created_at = models.DateTimeField(null=False, auto_now_add=True)
    closed_at = models.DateTimeField(null=True)
    cancelled_at = models.DateTimeField(null=True)

    class Meta:
        indexes = [
            models.Index(fields=['source_type', 'source_sym'], name='order_source_idx'),
            models.Index(fields=['target_type', 'target_sym'], name='order_target_idx'),
        ]


class AssetTickSummary(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=12, null=False, default=AssetType.STOCKS, choices=ASSET_TYPE_CHOICES)
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
