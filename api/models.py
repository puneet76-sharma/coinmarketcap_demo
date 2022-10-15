from django.db import models

# Create your models here.

class CoinMarket(models.Model):
    name = models.CharField(max_length=240)
    price = models.CharField(max_length=120)
    one_hour = models.CharField(max_length=120)
    twenty_four_hour = models.CharField(max_length=120)
    seven_days = models.CharField(max_length=120)
    market_cap = models.CharField(max_length=120)
    volume_24 = models.CharField(max_length=120)


    def __str__(self):
        return self.name


