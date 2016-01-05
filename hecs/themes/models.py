from django.db import models


class Theme(models.Model):
    name = models.CharField(max_length=30, blank=True, default='')
    x = models.IntegerField(null=True)
    y = models.IntegerField(null=True)
    color = models.CharField(max_length=20, blank=True, default='')

    def __str__(self):
        return self.name

