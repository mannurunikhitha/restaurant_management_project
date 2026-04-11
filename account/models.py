from django.db import models

# Create your models here.
class LoyaltyProgram(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True
    )
    points_required = models.IntegerField(
        unique=True
    )
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )
    description = models.TextField()
    def __str__(self):
        return self.name
