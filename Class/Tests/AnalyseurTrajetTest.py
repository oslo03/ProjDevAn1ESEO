import unittest

from Class.AnalyseurTrajets import AnalyseurTrajets
from Class.TrajetObserve import TrajetObserve
from Class.ReseauUrbain import ReseauUrbain
from Class.Distance import Distance


class AnalyseurTrajetTest(unittest.TestCase):

    def setUp(self):
        self.reseau = ReseauUrbain("reseau_test")  # Create a minimal test network

        self.reseau.ajouter_station("A")
        self.reseau.ajouter_station("B")
        self.reseau.ajouter_station("C")

        self.reseau.ajouter_route("A", "B", 10, 10)
        self.reseau.ajouter_route("B", "C", 10, 10)

    # Tested anomaly: loop (same station visited more than once)
    def test_detection_boucle(self):
        trajet = TrajetObserve("T1", ["A", "B", "A"], 20, 20)  # Create a trajectory with a loop

        analyseur = AnalyseurTrajets(self.reseau, [trajet])  # Create the analyzer
        anomalies = analyseur.detection_anomalies()          # Detect anomalies

        self.assertTrue(any("Boucle détectée" in a for a in anomalies))  # Check loop detection

    # Tested anomalies: missing route and theoretically impossible trajectory
    def test_route_manquante(self):
        trajet = TrajetObserve("T2", ["C", "A"], 50, 50)  # Create a trajectory with no direct route

        analyseur = AnalyseurTrajets(self.reseau, [trajet])  # Create the analyzer
        anomalies = analyseur.detection_anomalies()          # Detect anomalies

        self.assertTrue(any("Route manquante" in a for a in anomalies))        # Missing route detected
        self.assertTrue(any("impossible théoriquement" in a for a in anomalies))  # Impossible trajectory detected

    # Tested anomaly: inconsistent measured time (too high compared to theoretical)
    def test_temps_incoherent(self):
        trajet = TrajetObserve("T3", ["A", "B", "C"], 100, 20)  # Create a trajectory with excessive time

        analyseur = AnalyseurTrajets(self.reseau, [trajet])  # Create the analyzer
        anomalies = analyseur.detection_anomalies()          # Detect anomalies

        self.assertTrue(any("Temps mesuré incohérent" in a for a in anomalies))  # Check time inconsistency

    # Tested feature: correct theoretical distance and time computation
    def test_calcul_theorie_trajet_valide(self):
        trajet = TrajetObserve("T4", ["A", "B", "C"], 0, 0)  # Create a valid trajectory

        analyseur = AnalyseurTrajets(self.reseau, [trajet])  # Create the analyzer
        theorie = analyseur.calcul_theorie_trajet(trajet)   # Compute theoretical values

        self.assertEqual(theorie.distance_theorique, 20)     # Check theoretical distance
        self.assertEqual(theorie.temps_theorique, 20)        # Check theoretical time
        self.assertEqual(theorie.segments_inexistants, [])   # Check that no segment is missing

    # Tested feature: theoretical computation with a missing segment
    def test_calcul_theorie_trajet_inexistant(self):
        trajet = TrajetObserve("T5", ["C", "A"], 0, 0)  # Create a trajectory with a missing segment

        analyseur = AnalyseurTrajets(self.reseau, [trajet])  # Create the analyzer
        theorie = analyseur.calcul_theorie_trajet(trajet)   # Compute theoretical values

        self.assertEqual(theorie.distance_theorique, 0)      # Distance must be zero
        self.assertEqual(theorie.temps_theorique, 0)         # Time must be zero
        self.assertTrue(("C", "A") in theorie.segments_inexistants)  # Missing segment detected


if __name__ == "__main__":
    unittest.main()