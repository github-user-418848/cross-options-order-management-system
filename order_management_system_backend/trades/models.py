from django.db import models
from users.models import CustomUser  # Import your custom user model

SYMBOL_CHOICES = [
    ('AAPL', 'Apple Inc. (Stock)'),
    ('GOOGL', 'Alphabet Inc. (Google) (Stock)'),
    ('MSFT', 'Microsoft Corporation (Stock)'),
    ('SPY', 'SPDR S&P 500 ETF Trust (ETF)'),
    ('QQQ', 'Invesco QQQ Trust (ETF)'),
    ('GLD', 'SPDR Gold Trust (ETF)'),
    ('BTC', 'Bitcoin (Cryptocurrency)'),
    ('ETH', 'Ethereum (Cryptocurrency)'),
    ('XRP', 'Ripple (Cryptocurrency)'),
    ('EUR/USD', 'Euro/US Dollar (Forex)'),
    ('GBP/JPY', 'British Pound/Japanese Yen (Forex)'),
    ('USD/JPY', 'US Dollar/Japanese Yen (Forex)'),
    ('XAU', 'Gold (Commodity)'),
    ('CL', 'Crude Oil (Commodity)'),
    ('NG', 'Natural Gas (Commodity)'),
    ('SPX', 'S&P 500 Index Options (Options/Futures)'),
    ('ES', 'E-Mini S&P 500 Futures (Options/Futures)'),
    ('TLT', 'iShares 20+ Year Treasury Bond ETF (Bond)'),
    ('AGG', 'iShares Core U.S. Aggregate Bond ETF (Bond)'),
    ('DJI', 'Dow Jones Industrial Average (Index)'),
    ('IXIC', 'Nasdaq Composite Index (Index)'),
    ('S&P 500', 'Standard & Poor\'s 500 Index (Index)'),
    ('VTSAX', 'Vanguard Total Stock Market Index Fund (Mutual Fund)'),
    ('FBGRX', 'Fidelity Blue Chip Growth Fund (Mutual Fund)'),
]

BUY_SELL_CHOICES = [
    ('Buy', 'Buy'),
    ('Sell', 'Sell'),
]

class Trade(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_of_execution = models.DateField(auto_now_add=True)
    amount_of_shares_bought = models.PositiveIntegerField()
    symbol_of_shares = models.CharField(max_length=10, choices=SYMBOL_CHOICES)
    buy_sell = models.CharField(
        max_length=4,
        choices=BUY_SELL_CHOICES,
    )
    
    price_per_share = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount_paid = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def calculate_total_amount(self):
        if self.buy_sell == 'Buy':
            return self.amount_of_shares_bought * self.price_per_share
        elif self.buy_sell == 'Sell':
            return -1 * (self.amount_of_shares_bought * self.price_per_share)
        else:
            raise ValueError("Invalid buy_sell")

    def save(self, *args, **kwargs):
        self.total_amount_paid = self.calculate_total_amount()
        super(Trade, self).save(*args, **kwargs)
        
    def __str__(self):
        return f"Trade ID: {self.id}, Symbol: {self.symbol_of_shares}, User: {self.user_id}"