
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
import pandas as pd
import logging

from .models import Materiel

logger = logging.getLogger(__name__)

def validate_row_data(row, required_columns):
    """ Validates the data in the row. """
    if row[required_columns].isnull().all():
        logger.error(f"Row is entirely NaN: {row}")
        return False
    if row[required_columns].isnull().any():
        logger.error(f"Row has NaN values in required columns: {row}")
        return False
    return True

def import_excel(request):
    if request.method == 'POST':
        excel_file = request.FILES.get('excel_file')
        if not excel_file:
            logger.error("No file was uploaded.")
            return HttpResponseBadRequest("No file was uploaded.")

        try:
            data = pd.read_excel(excel_file, engine='openpyxl', header=0)
            data.dropna(how='all', inplace=True)  # Drop rows where all elements are NaN
            logger.info("Columns found in Excel file: %s", list(data.columns))
        except Exception as e:
            logger.error("Error reading file: %s", str(e), exc_info=True)
            return HttpResponseBadRequest(f"Error reading file: {str(e)}")

        required_columns = ['Services', 'NOM Prénom', 'Nom du compte', 'Mot de passe', 
                            'NOM MACHINE actuel', 'Type machine', 'ram installé', 'carte graphique']

        if not set(required_columns).issubset(set(data.columns)):
            missing = set(required_columns) - set(data.columns)
            logger.error("Missing columns in the Excel file: %s", missing)
            return HttpResponseBadRequest(f"Missing columns in the Excel file: {missing}")

        for index, row in data.iterrows():
            if not validate_row_data(row, required_columns):
                logger.error(f"Invalid data in row {index + 1}: {row}")
                continue  # Skip this row and continue with the next

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
                logger.error("Failed to create object at row %s: %s", index + 1, str(e), exc_info=True)
                return HttpResponseBadRequest(f"Failed to create object at row {index + 1}: {str(e)}")

        return HttpResponse("Importation réussie")
    else:
        return render(request, 'materiels/upload_form.html', {})

