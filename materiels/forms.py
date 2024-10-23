from django import forms
from .models import Materiel



class MaterielForm(forms.ModelForm):
    class Meta:
        model = Materiel
        fields = '__all__'
        widgets = {
            'Services': forms.Select(choices=Materiel.CONDITION_CHOICES),
        }
    labels = {
      'Services' : 'Services' ,
      'NOM_Prénom':'NOM Prénom',
      'Nom_du_compte': 'Nom_du_compte',
      'Mot_de_passe': 'Mot_de_passe',
      'NOM_MACHINE_actuel': 'NOM_MACHINE_actuel',
      'Type_machine' : 'Type_machine',
      'ram_installé': 'ram_installé',
      'carte_graphique': 'carte_graphique',
      'Emplacement': 'Emplacement',
      'Actions':'Actions'
    }
  
    widgets = {
      'Services': forms.TextInput(attrs={'class': 'form-control'}),
      'NOM_Prénom': forms.TextInput(attrs={'class': 'form-control'}),
      'Nom_du_compte': forms.TextInput(attrs={'class': 'form-control'}),
      'Mot_de_passe': forms.TextInput(attrs={'class': 'form-control'}),
      'NOM_MACHINE_actuel': forms.TextInput(attrs={'class': 'form-control'}),
      'Type_machine': forms.TextInput(attrs={'class': 'form-control'}),
      'ram_installé': forms.TextInput(attrs={'class': 'form-control'}),
      'carte_graphique' :  forms.TextInput(attrs={'class': 'form-control'}),
      'Emplacement' : forms.TextInput(attrs={'class': 'form-control'}),
      'Actions': forms.TextInput(attrs={'class': 'form-control'}),
    }
def __init__(self, *args, **kwargs):
        super(MaterielForm, self).__init__(*args, **kwargs)
        # Initialiser les choix pour type_d_ordinateur à partir du modèle
        self.fields['Services'].choices = Materiel.CONDITION_CHOICES