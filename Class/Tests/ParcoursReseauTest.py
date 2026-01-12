import unittest

from Class.ReseauUrbain import ReseauUrbain
from Class.ParcoursReseau import ParcoursReseau


class ParcoursReseauTest(unittest.TestCase):
    """
    Tests unitaires de la classe ParcoursReseau.

    Ces tests vérifient le bon fonctionnement des algorithmes :
    - BFS (parcours en largeur)
    - DFS (parcours en profondeur)

    Les cas normaux et les cas d’erreur sont couverts.
    """

    def setUp(self):
        """
        Création d’un réseau de test simple utilisé par tous les tests.

        Structure du réseau :
            A
           / \
          B   C
           \ /
            D
        """

        self.reseau = ReseauUrbain("reseau_test")

        # Ajout des stations
        self.reseau.ajouter_station("A")
        self.reseau.ajouter_station("B")
        self.reseau.ajouter_station("C")
        self.reseau.ajouter_station("D")

        # Ajout des routes
        self.reseau.ajouter_route("A", "B", 1, 1)
        self.reseau.ajouter_route("A", "C", 1, 1)
        self.reseau.ajouter_route("B", "D", 1, 1)
        self.reseau.ajouter_route("C", "D", 1, 1)

        # Création du module de parcours
        self.parcours = ParcoursReseau(self.reseau)

    # ======================================================
    # TESTS DU BFS
    # ======================================================

    def test_bfs_parcours_complet(self):
        """
        Vérifie que le BFS parcourt toutes les stations accessibles
        à partir de la station A.
        """

        resultat = self.parcours.bfs("A")

        # BFS doit visiter toutes les stations du réseau
        self.assertCountEqual(resultat, ["A", "B", "C", "D"])

        # La première station visitée doit être la station de départ
        self.assertEqual(resultat[0], "A")

    def test_bfs_station_inconnue(self):
        """
        Vérifie que le BFS lève une exception si la station de départ
        n’existe pas dans le réseau.
        """

        with self.assertRaises(ValueError):
            self.parcours.bfs("Z")

    def test_bfs_station_isolee(self):
        """
        Vérifie le comportement du BFS sur une station sans voisins.
        """

        self.reseau.ajouter_station("E")  # Station isolée
        resultat = self.parcours.bfs("E")

        # BFS doit uniquement retourner la station elle-même
        self.assertEqual(resultat, ["E"])

    # ======================================================
    # TESTS DU DFS
    # ======================================================

    def test_dfs_parcours_complet(self):
        """
        Vérifie que le DFS parcourt toutes les stations accessibles
        à partir de la station A.
        """

        resultat = self.parcours.dfs("A")

        # DFS doit visiter toutes les stations du réseau
        self.assertCountEqual(resultat, ["A", "B", "C", "D"])

        # La première station visitée doit être la station de départ
        self.assertEqual(resultat[0], "A")

    def test_dfs_station_inconnue(self):
        """
        Vérifie que le DFS lève une exception si la station de départ
        n’existe pas dans le réseau.
        """

        with self.assertRaises(ValueError):
            self.parcours.dfs("Z")

    def test_dfs_station_isolee(self):
        """
        Vérifie le comportement du DFS sur une station sans voisins.
        """

        self.reseau.ajouter_station("E")  # Station isolée
        resultat = self.parcours.dfs("E")

        # DFS doit uniquement retourner la station elle-même
        self.assertEqual(resultat, ["E"])


if __name__ == "__main__":
    unittest.main()
