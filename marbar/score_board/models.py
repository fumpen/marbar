from django.db import models


class ScoreUnit(models.Model):
    title = models.CharField(max_length=200, default="")
    points = models.IntegerField(default=0)
    placement = models.IntegerField(default=0)
    marbar = models.ForeignKey('management.MarBar', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
