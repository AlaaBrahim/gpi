from django.db import models
from django.db import models

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('resolved', 'Resolved'),
        ('non_attribue', 'Non Attribué'),
    ]
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
  
