from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ticket.models import Ticket, User
from django.shortcuts import render
from accounts.models import User  # Assurez-vous que l'import est correct
@login_required
def dashboard(request):
    if request.user.is_customer:
        tickets = Ticket.objects.filter(customer=request.user).count()
        active_tickets = Ticket.objects.filter(customer=request.user, is_resolved=False).count()
        closed_tickets = Ticket.objects.filter(customer=request.user, is_resolved=True).count()

        # Obtenez les tickets résolus
        resolved_tickets = Ticket.objects.filter(customer=request.user, is_resolved=True).order_by('-created_on')

        # Vérifiez les tickets résolus déjà affichés
        displayed_resolved_tickets = request.session.get('displayed_resolved_tickets', [])

        # Filtrez les tickets pour ne pas réafficher ceux qui ont déjà été affichés
        new_resolved_tickets = resolved_tickets.exclude(id__in=displayed_resolved_tickets)

        # Mettez à jour la session avec les nouveaux tickets résolus affichés
        request.session['displayed_resolved_tickets'] = list(resolved_tickets.values_list('id', flat=True))
       
        context = {
            'tickets': tickets,
            'active_tickets': active_tickets,
            'closed_tickets': closed_tickets,
            'resolved_tickets': new_resolved_tickets,
           
        }
        return render(request, 'dashboard/customer_dashboard.html', context)
    elif  request.user.is_engineer:
        pending_tickets = Ticket.objects.filter(status='Pending').order_by('-created_on')
        reclamation_tickets = Ticket.objects.filter(reclamation_date__isnull=False,status='Pending')
        context = {
        'pending_tickets': pending_tickets,
        'reclamation_tickets': reclamation_tickets,
        'tickets_pending': pending_tickets.count(),
        'tickets_resolved': Ticket.objects.filter(status='resolved').count(),
    }
        return render(request, 'dashboard/engineer_dashboard.html', context)

    elif request.user.is_superuser:
        tickets_pending = Ticket.objects.filter(status='Pending').count()
        tickets_resolved = Ticket.objects.filter(status='Resolved').count()
     
        context = {
            'tickets_pending': tickets_pending,
            'tickets_resolved': tickets_resolved,
       
        }
        return render(request, 'dashboard/admin_dashboard.html', context)





def dashboard_view(request):
    tickets_pending = Ticket.objects.filter(status='Pending').count()
    tickets_resolved = Ticket.objects.filter(status='Resolved').count()

    context = {
        'tickets_pending': tickets_pending,
        'tickets_resolved': tickets_resolved,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)









