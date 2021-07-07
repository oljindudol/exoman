from django.db import models

# Create your models here.


class Bschedule(models.Model):
    bdate = models.CharField(max_length=10)
    btime = models.CharField(max_length=5)
    bday = models.CharField(max_length=3)
    bbname = models.CharField(max_length=10)
    bone = models.CharField(max_length=12)
    btwo = models.CharField(max_length=12, default="", blank=True)
    bthree = models.CharField(max_length=12, default="", blank=True)
    bfour = models.CharField(max_length=12, default="", blank=True)
    bfive = models.CharField(max_length=12, default="", blank=True)
    bsix = models.CharField(max_length=12, default="", blank=True)
    bsisdeleted = models.CharField(max_length=1, default="0", blank=True)

    def __str__(self):
        return " ".join(
            [self.bdate, "(" + self.bday + ")", self.btime, self.bbname, self.bone]
        )
