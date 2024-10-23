# Le fichier models.py définit les modèles de données de l'application. Chaque modèle représente une table dans la base de données.
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('engineer', 'Engineer'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='engineer')
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_customer  = models.BooleanField(default=False)
    is_engineer = models.BooleanField(default=False)
    def __str__(self):
        return self.username
    

    