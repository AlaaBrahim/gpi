# models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
from django.utils import timezone
import datetime

User = get_user_model()

class Ticket(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    engineer = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='engineer', null=True, blank=True)
    ticket_id = models.CharField(max_length=15, unique=True)
    ticket_title = models.CharField(max_length=50)
    ticket_description = models.TextField()
    status = models.CharField(max_length=20, choices=( ('Pending', 'Pending'), ('Resolved', 'Resolved')), default='Pending')
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    is_resolved = models.BooleanField(default=False)
    notification_sent = models.BooleanField(default=False)

    reclamation_date = models.DateTimeField(null=True, blank=True)
    resolution_steps = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.ticket_title

    def is_due_for_reclamation(self):
        now = timezone.now()
        time_difference = now - self.created_on
        print(f"Current time: {now}")
        print(f"Ticket creation time: {self.created_on}")
        print(f"Time difference: {time_difference}")
        return time_difference > datetime.timedelta(minutes=3)  # Adjust to 1 day for production

print("Ticket model loaded")
