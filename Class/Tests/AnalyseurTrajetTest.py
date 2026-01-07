import unittest

from Class.AnalyseurTrajets import AnalyseurTrajets
from Class.TrajetObserve import TrajetObserve
from Class.ReseauUrbain import ReseauUrbain
from Class.ParcoursReseau import ParcoursReseau
from Class.Distance import Distance


class AnalyseurTrajetTest(unittest.TestCase):

    def setUp(self):
        self.reseau = ReseauUrbain("reseau_test")

        self.reseau.ajouter_station("A")
        self.reseau.ajouter_station("B")
        self.reseau.ajouter_station("C")

        self.reseau.ajouter_route("A", "B", 10, 10)
        self.reseau.ajouter_route("B", "C", 10, 10)

    # Tested anomaly: loop (same station visited more than once)
    def test_detection_boucle(self):
        trajet = TrajetObserve("T1", ["A", "B", "A"], 20, 20)

        analyseur = AnalyseurTrajets(self.reseau, [trajet])
        analyseur.parcours = ParcoursReseau(self.reseau)  # 🔧 dependency injection

        anomalies = analyseur.detection_anomalies()

        self.assertTrue(any("Boucle détectée" in a for a in anomalies))

    # Tested anomalies: missing route and theoretically impossible trajectory
    def test_route_manquante(self):
        trajet = TrajetObserve("T2", ["C", "A"], 50, 50)

        analyseur = AnalyseurTrajets(self.reseau, [trajet])
        analyseur.parcours = ParcoursReseau(self.reseau)  # 🔧 dependency injection

        anomalies = analyseur.detection_anomalies()

        self.assertTrue(any("Route manquante" in a for a in anomalies))
        self.assertTrue(any("impossible théoriquement" in a for a in anomalies))

    # Tested anomaly: inconsistent measured time (too high compared to theoretical)
    def test_temps_incoherent(self):
        trajet = TrajetObserve("T3", ["A", "B", "C"], 100, 20)

        analyseur = AnalyseurTrajets(self.reseau, [trajet])
        analyseur.parcours = ParcoursReseau(self.reseau)  # 🔧 dependency injection

        anomalies = analyseur.detection_anomalies()

        self.assertTrue(any("Temps mesuré incohérent" in a for a in anomalies))

    # Tested feature: correct theoretical distance and time computation
    def test_calcul_theorie_trajet_valide(self):
        trajet = TrajetObserve("T4", ["A", "B", "C"], 0, 0)

        analyseur = AnalyseurTrajets(self.reseau, [trajet])
        analyseur.parcours = ParcoursReseau(self.reseau)  # 🔧 dependency injection

        theorie = analyseur.calcul_theorie_trajet(trajet)

        self.assertEqual(theorie.distance_theorique, 20)
        self.assertEqual(theorie.temps_theorique, 20)
        self.assertEqual(theorie.segments_inexistants, [])

    # Tested feature: theoretical computation with a missing segment
    def test_calcul_theorie_trajet_inexistant(self):
        trajet = TrajetObserve("T5", ["C", "A"], 0, 0)

        analyseur = AnalyseurTrajets(self.reseau, [trajet])
        analyseur.parcours = ParcoursReseau(self.reseau)  # 🔧 dependency injection

        theorie = analyseur.calcul_theorie_trajet(trajet)

        self.assertEqual(theorie.distance_theorique, 0)
        self.assertEqual(theorie.temps_theorique, 0)
        self.assertTrue(("C", "A") in theorie.segments_inexistants)


if __name__ == "__main__":
    unittest.main()
