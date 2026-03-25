from django.db import models

# Create your models here.
class MenuCategory(models.Model):
    name=models.CharField(max_length=100,unique=True)
    def __str__(self):
        return self.name
    
class Restaurant(models.Model):
    name=models.CharField(max_length=255)
    address=models.TextField()
    has_delivery=models.BooleanField(default=False)
    def __str__(self):
        return self.name
    
class DailyOperatingHours(models.Model):
    day = models.CharField(max_length=10)
    open_time = models.TimeField()
    close_time = models.TimeField()
    def __str__(self):
        return f"{self.day}: {self.open_time} - {self.close_time}"