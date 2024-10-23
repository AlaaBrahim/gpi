
# heni win yab3eth admin ticket lel engineer 
# houni win tssir creation mata3 ticket 
from django import forms
from .models import Ticket

class CreateTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['ticket_title', 'ticket_description']

from django.core.mail import send_mail
from django.contrib import messages

class AdminNotificationMiddleware:
    def process_request(self, request):
        # Récupérer les messages avec le tag 'admin_notification'
        admin_messages = messages.get_messages(request)
        for message in admin_messages:
            if 'admin_notification' in message.tags:
                # Envoyer un e-mail à l'administrateur
                send_mail(
                    'Nouveau ticket créé',
                    message.message,
                    'from@example.com',  # Remplacez par votre adresse e-mail
                    ['adminadmin@gmail.com'],  # Remplacez par l'adresse e-mail de l'admin
                    fail_silently=True,
                )          



