import random
from django.test import TestCase
from .models import Materiel


class MaterielModelUnitTestCase(TestCase):
    def setUp(self):
        self.materiel = Materiel.objects.create(
            Services='Ref01',
            NOM_Prénom='aa',
            Nom_du_compte='Bob',
            Mot_de_passe='Smith',
            NOM_MACHINE_actuel='bob.smith@test.com',
            Type_machine='Smith',
            ram_installé='Computer Science',
            carte_graphique='127.0.0.1',
            Emplacement='127.0.0.1',
         
        )

    def test_materiel_model(self):
        data = self.materiel
        self.assertIsInstance(data, Materiel)
