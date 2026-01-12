import unittest
from Class.Distance import Distance


class TestDistance(unittest.TestCase):
    """
    Tests unitaires de la classe Distance.

    Ces tests vérifient :
    - l'initialisation correcte des attributs
    - le contenu de la représentation textuelle (__str__)
    """

    # TEST DU CONSTRUCTEUR
    def test_creation_distance(self):
        """Vérifie l'initialisation des attributs."""
        distance = Distance(20, 15, [("A", "B")])

        self.assertEqual(distance.distance_theorique, 20)
        self.assertEqual(distance.temps_theorique, 15)
        self.assertEqual(distance.segments_inexistants, [("A", "B")])

    # TEST AVEC LISTE DE SEGMENTS VIDE
    def test_aucun_segment_inexistant(self):
        """Vérifie le cas sans segment inexistant."""
        distance = Distance(30, 25, [])

        self.assertEqual(distance.segments_inexistants, [])

    # TEST DE LA MÉTHODE __str__()
    def test_str(self):
        """Vérifie la représentation textuelle."""
        distance = Distance(10, 8, [("B", "C")])

        resultat = str(distance)
        attendu = (
            "Distance théorique: 10, "
            "Temps théorique: 8, "
            "Segments inexistants: [('B', 'C')]"
        )

        self.assertEqual(resultat, attendu)

    # TEST DE COHÉRENCE DES DONNÉES
    def test_types_attributs(self):
        """
        Vérifie que les attributs sont du type attendu.
        """
        distance = Distance(12, 9, [])

        self.assertIsInstance(distance.distance_theorique, (int, float))
        self.assertIsInstance(distance.temps_theorique, (int, float))
        self.assertIsInstance(distance.segments_inexistants, list)


if __name__ == "__main__":
    unittest.main()
