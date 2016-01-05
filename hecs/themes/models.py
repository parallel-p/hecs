from django.db import models


class Theme(models.Model):
    name = models.CharField(max_length=30, blank=True, default='')
    x = models.IntegerField(null=True)
    y = models.IntegerField(null=True)
    color = models.CharField(max_length=6, blank=True, default='')

    def __str__(self):
        return self.name


class ReferenceGroup(models.Model):
    name = models.CharField(max_length=30)  # theory, video, problems etc
    icon = models.CharField(max_length=16)  # image filename
    
    def __str__(self):
        return self.name


class ReferenceTarget(models.Model):
    name = models.CharField(max_length=30)  # foxford, habr, informatics
    color = models.CharField(max_length=16)
    
    def __str__(self):
        return self.name


class Reference(models.Model):
    theme = models.ForeignKey('Theme')
    group = models.ForeignKey('ReferenceGroup')
    target = models.ForeignKey('ReferenceTarget')
    name = models.CharField(max_length=30)
    href = models.CharField(max_length=256)
    
    def __str__(self):
        return str(self.target) + ': ' + self.name