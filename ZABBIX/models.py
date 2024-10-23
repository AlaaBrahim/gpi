
from django.db import models

class Hote(models.Model):
    nom = models.CharField(max_length=100)
    adresse_ip = models.CharField(max_length=15)

    def __str__(self):
        return self.nom
