#Le fichier views.py contient les vues de l'application. Une vue reçoit les requêtes HTTP, traite les données, et renvoie des réponses HTTP.

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.conf import settings
from .form import  RegisterCustomerForm, RegisterUserForm
from accounts.form import RegisterUserForm
from django.contrib.auth.decorators import login_required
from .models import User  # Importez le modèle utilisateur personnalisé
import logging
from django.contrib.auth.models import User
logger = logging.getLogger(__name__)



User = get_user_model()
#pour inscription normal
def register_customer(request):
    if request.method == 'POST':
        form = RegisterCustomerForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)#Créer une instance sans l'enregistrer,Cela vous donne la flexibilité de modifier l'instance ou d'effectuer d'autres actions avant l'enregistrement final. 
            user.is_customer = True
            user.username = user.email
            user.is_active = False  # Le compte est initialement inactif
            user.save()

            # Envoi de l'e-mail d'activation
            subject = 'Activation de votre compte'
            message = 'Cliquez sur ce lien pour activer votre compte : {}/activate/{}'.format(request.build_absolute_uri('/'), user.id)#crée un message contenant un lien d'activation pour un utilisateur
            from_email = settings.EMAIL_HOST_USER#Cette valeur est généralement configurée dans les paramètres de votre projet Django (settings.py).
            to_email = user.email
            send_mail(subject, message, from_email, [to_email])

            messages.success(request, 'Un e-mail d\'activation a été envoyé à votre adresse.')
            return redirect('login')
        else:
            messages.warning(request, 'Quelque chose s\'est mal passé. Veuillez vérifier les erreurs du formulaire.')
            return redirect('register-customer')
    else:
        form = RegisterCustomerForm()#une nouvelle instance du formulaire RegisterCustomerForm
    return render(request, 'accounts/register_customer.html', {'form': form})

#pour login 
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')#Récupération des données du formulaire 
        password = request.POST.get('password')#Récupération des données du formulaire 
        user = authenticate(request, username=username, password=password)#La fonction authenticate vérifie si les informations d'identification fournies sont correctes. S
        
        if user is not None and user.is_active:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.warning(request, 'Quelque chose s est mal passé. Veuillez vérifier les erreurs du formulaire')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')
    
#pour out 
def logout_user(request):
    logout(request)#La fonction logout(request) dans Django est utilisée pour déconnecter un utilisateur actuellement connecté.
    messages.success(request, 'La session active est terminée. connectez-vous pour continuer')
    return redirect('login')



#activation de compte

def activate_account(request, user_id):
    user = get_object_or_404(User, pk=user_id)#Cette ligne tente de récupérer l'utilisateur avec l'ID fourni (user_id). Si aucun utilisateur correspondant n'est trouvé, une erreur 404 (page non trouvée) est levée.

    if request.method == 'POST':#Cette condition vérifie si la méthode de la requête est POST, ce qui signifie que le formulaire d'activation a été soumis. Si la méthode n'est pas POST, la fonction passera directement à l'affichage du formulaire.
        role = request.POST.get('role')

        if role == 'customer' or role == 'engineer':
            user.role = role
            user.is_active = True
            user.save()
            messages.success(request, f'Le compte de {user.username} a été activé.')
            return redirect('login')  # Rediriger vers la page de connexion
        else:
            messages.error(request, 'Veuillez sélectionner un rôle valide.')

    return render(request, 'accounts/activate_account.html', {'user': user})

#pour l'admin ajouter un memebre
User = get_user_model()

def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data.get('role')# Elle permet de traiter les informations soumises par l'utilisateur de manière sécurisée et structurée
            user.username = user.email
            if role == 'admin':
                user.is_superuser = True
                user.is_engineer = False
                user.is_staff = True
            elif role == 'engineer':
                user.is_engineer = True
                user.is_superuser = False
                
                user.is_staff = False
            user.save()
            messages.success(request, "Le nouvel utilisateur a été ajouté et activé avec succès.")
            return redirect('dashboard') 
        else:
            messages.error(request, "Quelque chose s'est mal passé. Veuillez vérifier les erreurs du formulaire.")
    else:
        form = RegisterUserForm()
    return render(request, 'accounts/register_user.html', {'form': form})





#ajouter un user(admin ,technicien ,employer)
@login_required
def user_list(request):
    users = User.objects.all()
    for user in users:
        if user.is_superuser:
            user.role = 'Admin'
        elif user.is_engineer:
            user.role = 'Engineer'
        elif user.is_customer:
            user.role = 'Customer'
    return render(request, 'accounts/user_liste.html', {'users': users})

#supprimer un user
@login_required#Vérification de l'authentification :
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, 'L\'utilisateur a été supprimé avec succès.')
    return redirect('user_list')  # Assurez-vous que ce nom correspond à votre vue de liste d'utilisateurs
