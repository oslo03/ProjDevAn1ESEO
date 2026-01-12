import unittest
from Class.Station import Station


class TestStation(unittest.TestCase):
    """
    Tests unitaires de la classe Station.

    Ces tests vérifient :
    - l'initialisation correcte des attributs
    - le comportement des méthodes d'affichage
    """

    # TEST DU CONSTRUCTEUR
    def test_creation_station(self):
        """Vérifie la création d'une station avec ses attributs."""
        station = Station(1, "Gare")

        self.assertEqual(station.id, 1)
        self.assertEqual(station.nom, "Gare")

    # TEST DE LA MÉTHODE affichage()
    def test_affichage(self):
        """Vérifie la méthode affichage()."""
        station = Station(2, "Centre")

        resultat = station.affichage()
        attendu = "Station Centre ID: 2"

        self.assertEqual(resultat, attendu)

    # TEST DE LA MÉTHODE __str__()
    def test_str(self):
        """Vérifie la représentation texte (__str__)."""
        station = Station(3, "Universite")

        resultat = str(station)
        attendu = "Station Universite ID: 3"

        self.assertEqual(resultat, attendu)

    # TEST DE COHÉRENCE AFFICHAGE / STR
    def test_affichage_et_str_identiques(self):
        """
        Vérifie que les deux méthodes retournent la même chaîne.
        """
        station = Station(4, "Aeroport")

        self.assertEqual(station.affichage(), str(station))


if __name__ == "__main__":
    unittest.main()
