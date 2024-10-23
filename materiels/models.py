from django.db import models

class Materiel(models.Model):
    CONDITION_CHOICES = [
        ('direction', 'Direction'),
        ('enedid', 'Enedid'),
        ('lidar', 'Lidar'),
        ('memoris', 'Memoris'),
        ('mosaiquage', 'Mosaiquage'),
        ('patrimoine', 'Patrimoine'),
        ('photogrammétrie', 'Photogrammétrie'),
        ('secétariat', 'Secétariat'),
        ('topographie', 'Topographie'),
        ('blanks', 'Blanks'),
    ]
    Services = models.CharField(max_length=255, null=True)
    
    NOM_Prénom = models.CharField(max_length=255, default='Default Name')
    Nom_du_compte = models.CharField(max_length=255)
    Mot_de_passe = models.CharField(max_length=255)
    NOM_MACHINE_actuel = models.CharField(max_length=255, null=True)
    Type_machine = models.CharField(max_length=255)
    ram_installé = models.CharField(max_length=255)
    Carte_graphique = models.CharField(max_length=255, null=True)
    Emplacement = models.CharField(max_length=255)
    

    def __str__(self):
        return f'{self.NOM_Prénom} {self.Mot_de_passe}'
