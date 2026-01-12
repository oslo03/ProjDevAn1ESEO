import unittest
from Class.TrajetObserve import TrajetObserve


class TestTrajetObserve(unittest.TestCase):
    """
    Tests unitaires de la classe TrajetObserve.

    Ces tests vérifient que :
    - un trajet observé est correctement initialisé
    - la conversion en liste chaînée fonctionne correctement
    - l’ordre des stations est conservé
    """

    def test_conversion_liste_chainee(self):
        """
        Teste la conversion d’un trajet observé en liste chaînée.

        On crée un trajet avec :
        - un identifiant
        - une liste de stations dans un ordre précis
        - un temps et une distance mesurés

        Puis on vérifie que la liste chaînée générée
        contient exactement les stations dans le bon ordre.
        """

        # Création d’un trajet observé avec deux stations
        trajOb1 = TrajetObserve(
            1,
            ["Erasme", "Piscine Olympique"],
            12,
            2
        )

        # Conversion de la liste de stations en liste chaînée
        liste_chainee = trajOb1.Conv_Liste_Chainee()

        # Vérification de l'affichage de la liste chaînée
        # L’ordre des stations doit être strictement respecté
        self.assertEqual(
            "Erasme Piscine Olympique",
            liste_chainee.affichage()
        )


if __name__ == "__main__":
    unittest.main()
