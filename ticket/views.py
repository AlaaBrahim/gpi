from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.db.utils import IntegrityError
import pytz
from django.utils import timezone
from ticket.models import  Ticket
from ticket.form import CreateTicketForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from ticket.models import Ticket
from django.conf import settings

import random
import string

@login_required
# pour customer creer un ticket
def create_ticket(request):
    if request.method == 'POST':
        form = CreateTicketForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.customer = request.user
            while not var.ticket_id:
                id = ''.join(random.choices(string.digits, k=6))
                try:
                    var.ticket_id = id
                    var.save()
             
                   #pour envoyer un mail
                    subject = f'{var.ticket_title} #{var.ticket_id}'
                    message = 'Merci davoir créé un ticket'
                    email_from = 'admin12@gmail.com'
                    recipient_list = [request.user.email, ]
                    #send_mail(subject, message, email_from, recipient_list)
                    messages.success(request, 'Votre ticket a été soumis')
                    return redirect('dashboard')
                except IntegrityError:
                    continue
        else:
    
            messages.warning(request," Quelque chose est mal passé")
            return redirect('create-ticket')
    else:
        form = CreateTicketForm()
    context = {'form': form}
    return render(request, 'ticket/create_ticket.html', context)



# les ticket en attente pour engineer
    
  

# les ticket resolus pour customer
def customer_resolved_tickets(request):
    tickets = Ticket.objects.filter(customer=request.user, is_resolved=True).order_by('-created_on')
    context = {'tickets':tickets}
    return render(request, 'ticket/customer_resolved_tickets.html', context)  


def engineer_active_tickets(request):
    tickets = Ticket.objects.filter(engineer=request.user, is_resolved=False).order_by('-created_on')
    context = {'tickets':tickets}
    return render(request, 'ticket/engineer_active_tickets.html', context)    


#les ticket resolus pour engineer
def engineer_resolved_tickets(request):
    tickets = Ticket.objects.filter( is_resolved=True)
    return render(request, 'ticket/engineer_resolved_tickets.html', {'tickets': tickets})

#les details pour chaque ticket  
def ticket_details(request, ticket_id):
    ticket = get_object_or_404(Ticket, ticket_id=ticket_id)
    context = {'ticket': ticket}
    tunis_tz = pytz.timezone('Africa/Tunis')
    ticket.created_on = ticket.created_on.astimezone(tunis_tz)
    ticket.last_modified = ticket.last_modified.astimezone(tunis_tz)
    return render(request, 'ticket/ticket_details.html', context)
   
#ticket en attente pour engineer
def ticket_queue(request):
    tickets = Ticket.objects.filter(is_resolved=False).order_by('-created_on')
    context = {'tickets':tickets}
    return render(request, 'ticket/engineer_active_tickets.html', context)

 
#engineer resolu ticket

def resolve_ticket(request, ticket_id):
    ticket = Ticket.objects.get(ticket_id=ticket_id)
    if request.method == 'POST':
        rs = request.POST.get('rs')
        ticket.resolution_steps = rs
        ticket.is_resolved = True 
        ticket.status = 'Resolved'
        ticket.save()
        messages.success(request, 'le ticket est maintenant résolu et clôturé')
        return redirect('dashboard')

#historique pour engineer   
def issue_history(request):
    tickets = Ticket.objects.all()
    context = {'tickets':tickets}
    return render(request, 'ticket/issue_history.html', context)
#admin envoyer reclamation
def send_reclamation(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if ticket.is_due_for_reclamation():
        ticket.reclamation_date = timezone.now()
        ticket.save()
        messages.success(request, "Réclamation envoyée à l'ingénieur.")
    else:
        messages.warning(request, "Le ticket n'a pas encore dépassé un jour.")
    return redirect('dashboard')
#les reclamation de engineer
def engineer_dashboard(request):
    reclamation_tickets = Ticket.objects.filter(reclamation_date__isnull=False)
    context = {
        'reclamation_tickets': reclamation_tickets,
    }
    return render(request, 'dashboard/engineer_dashboard.html', context)