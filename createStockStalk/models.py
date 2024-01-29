from django.db import models

# Create your models here.

class StockStalk(models.Model):
    stock_ticker = models.CharField(max_length = 50)
    target_stock_price = models.IntegerField()
    email_to_notify = models.CharField(max_length = 200)

    # This method will define what should be printed when the class is converted to a string.
    def __str__(self):
        return f"{self.stock_ticker} - Target Price: {self.target_stock_price} and email to be notified: {self.email_to_notify}"