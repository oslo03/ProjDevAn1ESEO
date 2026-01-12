import unittest
from Class.ReseauUrbain import ReseauUrbain


class TestReseauUrbain(unittest.TestCase):
    """
    Tests unitaires de la classe ReseauUrbain.

    Les tests vérifient :
    - la construction du réseau
    - l’ajout de stations et de routes
    - la cohérence des matrices d’adjacence
    - la gestion des erreurs
    """

    # INITIALISATION COMMUNE
    def setUp(self):
        self.reseau = ReseauUrbain("reseau_test")

    # TESTS DE BASE
    def test_creation_reseau(self):
        """Vérifie la création d’un réseau vide."""
        self.assertEqual(self.reseau.nom, "reseau_test")
        self.assertEqual(len(self.reseau.stations), 0)
        self.assertEqual(self.reseau.matrice_distances, [])
        self.assertEqual(self.reseau.matrice_temps, [])

    # TESTS D’AJOUT DE STATIONS
    def test_ajout_station(self):
        """Vérifie l’ajout d’une station."""
        self.reseau.ajouter_station("A")

        self.assertEqual(len(self.reseau.stations), 1)
        self.assertIn("A", self.reseau.index_par_nom)
        self.assertEqual(self.reseau.index_par_nom["A"], 0)

        self.assertEqual(self.reseau.matrice_distances, [[-1]])
        self.assertEqual(self.reseau.matrice_temps, [[-1]])

    def test_ajout_station_double(self):
        """Vérifie qu’une station déjà existante n’est pas ajoutée deux fois."""
        self.reseau.ajouter_station("A")
        self.reseau.ajouter_station("A")

        self.assertEqual(len(self.reseau.stations), 1)

    def test_ajout_plusieurs_stations(self):
        """Vérifie la cohérence des matrices après plusieurs ajouts."""
        self.reseau.ajouter_station("A")
        self.reseau.ajouter_station("B")
        self.reseau.ajouter_station("C")

        self.assertEqual(len(self.reseau.stations), 3)
        self.assertEqual(len(self.reseau.matrice_distances), 3)
        self.assertEqual(len(self.reseau.matrice_distances[0]), 3)

    # TESTS D’AJOUT DE ROUTES
    def test_ajout_route(self):
        """Vérifie l’ajout d’une route bidirectionnelle."""
        self.reseau.ajouter_station("A")
        self.reseau.ajouter_station("B")

        self.reseau.ajouter_route("A", "B", 10, 5)

        i = self.reseau.index_par_nom["A"]
        j = self.reseau.index_par_nom["B"]

        self.assertEqual(self.reseau.matrice_distances[i][j], 10)
        self.assertEqual(self.reseau.matrice_distances[j][i], 10)
        self.assertEqual(self.reseau.matrice_temps[i][j], 5)
        self.assertEqual(self.reseau.matrice_temps[j][i], 5)

    def test_ajout_route_station_inconnue(self):
        """Vérifie qu’une erreur est levée si une station n’existe pas."""
        self.reseau.ajouter_station("A")

        with self.assertRaises(ValueError):
            self.reseau.ajouter_route("A", "B", 10, 5)

    # TESTS DE LA MÉTHODE voisins
    def test_voisins(self):
        """Vérifie la liste des voisins d’une station."""
        self.reseau.ajouter_station("A")
        self.reseau.ajouter_station("B")
        self.reseau.ajouter_station("C")

        self.reseau.ajouter_route("A", "B", 10, 5)
        self.reseau.ajouter_route("A", "C", 8, 4)

        voisins = self.reseau.voisins("A")

        self.assertCountEqual(voisins, ["B", "C"])

    def test_voisins_station_inconnue(self):
        """Vérifie qu’une erreur est levée pour une station inconnue."""
        with self.assertRaises(ValueError):
            self.reseau.voisins("X")

    # TEST DE REPRÉSENTATION TEXTE
    def test_str(self):
        """Vérifie la représentation textuelle du réseau."""
        self.reseau.ajouter_station("A")
        self.reseau.ajouter_station("B")

        self.assertEqual(
            str(self.reseau),
            "Réseau reseau_test avec 2 stations"
        )


if __name__ == "__main__":
    unittest.main()
