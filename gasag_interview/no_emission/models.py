from django.db import models

# Create your models here.
class Emission(models.Model):
    time_date=models.CharField(max_length=25)
    station_id=models.IntegerField()
    emission=models.IntegerField()

    def __str__(self):
        return self.time_date + " " +str(self.emission) + " " + str(self.station_id)
