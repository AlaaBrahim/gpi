#Le fichier forms.py contient les définitions des formulaires de l'application. Les formulaires permettent de valider et de nettoyer les données soumises par les utilisateurs.
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


#register normal
User = get_user_model()
class RegisterCustomerForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']
#activation
class AccountActivationForm(forms.Form):
    ROLE_CHOICES = [
        ('is_customer', 'is_customer'),
     
    ]
 
#user ajouter par admin
User = get_user_model()

class RegisterUserForm(forms.ModelForm):
    password1 = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmer mot de passe', widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, label="Rôle")

    class Meta:
        model = User
        fields = [ 'email',  'role']
#hedha bech ya3mel activation direct lel compte mi
    
    def save(self, commit=True):
        user = super(RegisterUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = True

        if self.cleaned_data['role'] == 'admin':
            user.is_staff = True
            user.is_superuser = True
        elif self.cleaned_data['role'] == 'engineer':
            user.is_staff = False
            user.is_superuser = False

        if commit:
            user.save()
        return user
