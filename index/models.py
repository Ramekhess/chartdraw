from django.db import models


class DFInput(models.Model):
    nom = models.CharField(max_length=250)
    file_path = models.CharField(max_length=500)
    vars = models.CharField(max_length=1000)
    vars_count = models.IntegerField()
    describe_path = models.CharField(max_length=500)
    file_to_path = models.CharField(max_length=500)
