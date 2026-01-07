import unittest

from Class.AnalyseurTrajets import AnalyseurTrajets
from Class.TrajetObserve import TrajetObserve
from Class.ReseauUrbain import ReseauUrbain


class AnalyseurTrajetTest(unittest.TestCase):

    def setUp(self):
        self.reseau = ReseauUrbain("reseau_test")

        self.reseau.ajouter_station("A")
        self.reseau.ajouter_station("B")
        self.reseau.ajouter_station("C")

        self.reseau.ajouter_route("A", "B", 10, 10)
        self.reseau.ajouter_route("B", "C", 10, 10)

    # Anomalie testée : boucle (station visitée plusieurs fois dans un même trajet)
    def test_detection_boucle(self):
        trajet = TrajetObserve(
            "T1",
            ["A", "B", "A"],
            20,
            20
        )

        analyseur = AnalyseurTrajets(self.reseau, [trajet])
        anomalies = analyseur.detection_anomalies()

        self.assertTrue(any("Boucle détectée" in a for a in anomalies))

    # Anomalies testées :
    # - route inexistante entre deux stations
    # - trajet impossible théoriquement
    def test_route_manquante(self):
        trajet = TrajetObserve(
            "T2",
            ["C", "A"],
            50,
            50
        )

        analyseur = AnalyseurTrajets(self.reseau, [trajet])
        anomalies = analyseur.detection_anomalies()

        self.assertTrue(any("Route manquante" in a for a in anomalies))
        self.assertTrue(any("impossible théoriquement" in a for a in anomalies))

    # Anomalie testée : temps mesuré incohérent (> 30 % du temps théorique)
    def test_temps_incoherent(self):
        trajet = TrajetObserve(
            "T3",
            ["A", "B", "C"],
            100,
            20
        )

        analyseur = AnalyseurTrajets(self.reseau, [trajet])
        anomalies = analyseur.detection_anomalies()

        self.assertTrue(any("Temps mesuré incohérent" in a for a in anomalies))


if __name__ == "__main__":
    unittest.main()
