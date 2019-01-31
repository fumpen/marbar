from django.db import models
from django.contrib.auth.models import User


class MarBar(models.Model):
    title = models.CharField(max_length=200, default="")
    banner = models.ImageField(upload_to='banners/',
                               verbose_name='banner', blank=True)
    user = models.ManyToManyField(User)
    end_date = models.DateTimeField(blank=False)
    is_active = models.BooleanField(default=False, blank=False)

    def __str__(self):
        return self.title


class Event(models.Model):
    models.ForeignKey(MarBar, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="")
    info = models.TextField(max_length=200, default="")
    start_date = models.DateTimeField(auto_now_add=True, blank=False)
    end_date = models.DateTimeField(auto_now_add=start_date, blank=False)

    def __str__(self):
        return self.title
