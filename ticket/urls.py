from django.urls import path
from . import views
from django.urls import path

urlpatterns = [
    path('create-ticket/', views.create_ticket, name='create-ticket'),
 
    path('customer-resolved-tickets/', views.customer_resolved_tickets, name='customer-resolved-tickets'),
    path('reclamation/<int:ticket_id>/', views.send_reclamation, name='send_reclamation'),
    path('ticket-details/<str:ticket_id>/', views.ticket_details, name='ticket-details'),
   
    path('ticket-queue/', views.ticket_queue, name='ticket-queue'), #les tickets qui sont en attentz pour engineer
    path('engineer-resolved-tickets/', views.engineer_resolved_tickets, name='engineer-resolved-tickets'),
    path('resolve-ticket/<str:ticket_id>/', views.resolve_ticket, name='resolve-ticket'),
    path('issue-history/', views.issue_history, name='issue-history'),
    
    
   

]