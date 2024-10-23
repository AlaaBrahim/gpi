from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from materiels.import_excel import validate_row_data
from .models import Materiel
from .forms import MaterielForm
from django.http import HttpResponse, HttpResponseBadRequest
import pandas as pd
import logging
from .models import Materiel
from django.contrib import messages
import pandas as pd
from django.http import HttpResponse
from .models import Materiel
logger = logging.getLogger(__name__)


def add(request):
    if request.method == 'POST':
        form = MaterielForm(request.POST, request.FILES)
        if form.is_valid():
            materiel = form.save(commit=False)
            materiel.save()
            form.save_m2m()  
            messages.success(request, 'Le nouveau matériel a été ajouté avec succès.')
            return render(request, 'materiels/add.html', {
                'form': MaterielForm(),
                'success': True
            })
    else:
        form = MaterielForm()
    return render(request, 'materiels/add.html', {'form': form})
def index(request):
    service_query = request.GET.get('service', '')
    materiels = Materiel.objects.filter(Services=service_query) if service_query else Materiel.objects.all()
    services = Materiel.objects.values_list('Services', flat=True).distinct()
    return render(request, 'index.html', {
        'materiels': materiels,
        'services': services,
        'current_service': service_query
    })

def import_excel(request):
    if request.method == 'POST':
        excel_file = request.FILES.get('excel_file')
        if not excel_file:
            logger.error("Aucun fichier n'a été téléchargé.")
            return HttpResponseBadRequest("Aucun fichier n'a été téléchargé.")

        try:
            data = pd.read_excel(excel_file, engine='openpyxl', header=0)
            data.dropna(how='all', inplace=True) 
            logger.info("Colonnes trouvées dans le fichier Excel: %s", list(data.columns))
        except Exception as e:
            logger.error("Erreur de lecture du fichier: %s", str(e), exc_info=True)
            return HttpResponseBadRequest(f"Erreur de lecture du fichier: {str(e)}")

        required_columns = ['Services', 'NOM Prénom', 'Nom du compte', 'Mot de passe', 
                            'NOM MACHINE actuel', 'Type machine', 'ram installé', 'carte graphique']

        if not set(required_columns).issubset(set(data.columns)):
            missing = set(required_columns) - set(data.columns)
            logger.error("Colonnes manquantes dans le fichier Excel: %s", missing)
            return HttpResponseBadRequest(f"Colonnes manquantes dans le fichier Excel: {missing}")

        for index, row in data.iterrows():
            if not validate_row_data(row, required_columns):
                logger.error(f"Données invalides dans la ligne {index + 1}: {row}")
                continue  

            try:
                Materiel.objects.create(
                    Services=row['Services'],
                    NOM_Prénom=row['NOM Prénom'],
                    Nom_du_compte=row['Nom du compte'],
                    Mot_de_passe=row['Mot de passe'],
                    NOM_MACHINE_actuel=row['NOM MACHINE actuel'],
                    Type_machine=row['Type machine'],
                    ram_installé=row['ram installé'],
                    Carte_graphique=row['carte graphique']
                )
            except Exception as e:
                logger.error("Échec de la création de l'objet sur la ligne %s: %s", index + 1, str(e), exc_info=True)
                return HttpResponseBadRequest(f"Échec de la création de l'objet sur la ligne {index + 1}: {str(e)}")

        return HttpResponse("Importation réussie")
    else:
        return render(request, 'materiels/upload_form.html', {})

def index(request):
    service_query = request.GET.get('service', '')
    if service_query:
        materiels = Materiel.objects.filter(Services=service_query)
    else:
        materiels = Materiel.objects.all()

    services = Materiel.objects.order_by('Services').values_list('Services', flat=True).distinct()
    return render(request, 'index.html', {'materiels': materiels, 'services': services})


def index(request):
  return render(request, 'materiels/index.html', {
    'materiels': Materiel.objects.all()
  })


def view_materiel(request, id):
  return HttpResponseRedirect(reverse('index'))





def edit(request, id):
  if request.method == 'POST':
    materiel = Materiel.objects.get(pk=id)
    form = MaterielForm(request.POST, instance=materiel)
    if form.is_valid():
      form.save()
      return render(request, 'materiels/edit.html', {
        'form': form,
        'success': True
      })
  else:
    materiel = Materiel.objects.get(pk=id)
    form = MaterielForm(instance=materiel)
  return render(request, 'materiels/edit.html', {
    'form': form
  })


def delete(request, id):
  if request.method == 'POST':
    materiel = Materiel.objects.get(pk=id)
    materiel.delete()
  return HttpResponseRedirect(reverse('index'))


def export_materiel_to_excel(request):
    materiels = Materiel.objects.all()
    data = []
    for materiel in materiels:
        data.append({
            'Services': materiel.Services,
            'NOM_Prénom': materiel.NOM_Prénom,
            'Nom_du_compte': materiel.Nom_du_compte,
            'Mot_de_passe': materiel.Mot_de_passe,
            'NOM_MACHINE_actuel': materiel.NOM_MACHINE_actuel,
            'Type_machine': materiel.Type_machine,
            'ram_installé': materiel.ram_installé,
            'Carte_graphique': materiel.Carte_graphique,
            'Emplacement': materiel.Emplacement,
        })
    
    df = pd.DataFrame(data)
    
    # Créez une réponse HTTP avec un type de contenu Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=materiels.xlsx'
    
    # Utilisez pandas pour écrire le fichier Excel
    with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Materiels', index=False)
    
    return response