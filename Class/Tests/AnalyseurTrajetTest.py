import unittest

from Class.AnalyseurTrajets import AnalyseurTrajets
from Class.TrajetObserve import TrajetObserve
from Class.ReseauUrbain import ReseauUrbain
from Class.ParcoursReseau import ParcoursReseau


class AnalyseurTrajetTest(unittest.TestCase):
    """
    Tests unitaires complets de la classe AnalyseurTrajets.

    Chaque test cible une anomalie précise afin de vérifier que :
    - l’anomalie est bien détectée
    - elle est correctement classée (FORMAT, LOGIQUE ou MESURE)
    """

    def setUp(self):
        # Initialisation d’un réseau simple et cohérent
        # utilisé par l’ensemble des tests
        self.reseau = ReseauUrbain("reseau_test")

        self.reseau.ajouter_station("A")
        self.reseau.ajouter_station("B")
        self.reseau.ajouter_station("C")

        self.reseau.ajouter_route("A", "B", 10, 10)
        self.reseau.ajouter_route("B", "C", 10, 10)

    # ===============================
    # TESTS DES ANOMALIES DE FORMAT
    # ===============================

    def test_aucune_station(self):
        # Teste le cas d’un trajet sans aucune station.
        # Ce cas correspond à une ligne vide ou corrompue dans le CSV.
        trajet = TrajetObserve("F1", [], 10, 10)

        analyseur = AnalyseurTrajets(self.reseau, [trajet])
        analyseur.parcours = ParcoursReseau(self.reseau)

        anomalies = analyseur.detection_anomalies()

        # Vérifie que l’anomalie est bien détectée dans la catégorie FORMAT
        self.assertIn("Aucune station renseignée", anomalies["F1"]["FORMAT"][0])

    def test_une_seule_station(self):
        # Teste un trajet ne contenant qu’une seule station.
        # Un tel trajet ne représente aucun déplacement réel.
        trajet = TrajetObserve("F2", ["A"], 10, 10)

        analyseur = AnalyseurTrajets(self.reseau, [trajet])
        analyseur.parcours = ParcoursReseau(self.reseau)

        anomalies = analyseur.detection_anomalies()

        # Vérifie la détection de l’anomalie de format
        self.assertTrue(
            any("Une seule station" in a for a in anomalies["F2"]["FORMAT"])
        )

    def test_station_inconnue(self):
        # Teste la présence d’une station absente du réseau.
        # Cela simule une erreur de saisie dans le CSV.
        trajet = TrajetObserve("F3", ["A", "D"], 10, 10)

        analyseur = AnalyseurTrajets(self.reseau, [trajet])
        analyseur.parcours = ParcoursReseau(self.reseau)

        anomalies = analyseur.detection_anomalies()

        # Vérifie que la station inconnue est bien signalée
        self.assertTrue(
            any("Station inconnue" in a for a in anomalies["F3"]["FORMAT"])
        )

    def test_valeurs_manquantes(self):
        # Teste l’absence de valeurs mesurées (temps ou distance).
        # Sans ces données, aucune comparaison avec la théorie n’est possible.
        trajet = TrajetObserve("F4", ["A", "B"], None, 10)

        analyseur = AnalyseurTrajets(self.reseau, [trajet])
        analyseur.parcours = ParcoursReseau(self.reseau)

        anomalies = analyseur.detection_anomalies()

        # Vérifie que l’anomalie de données manquantes est détectée
        self.assertTrue(
            any("Valeurs mesurées manquantes" in a for a in anomalies["F4"]["FORMAT"])
        )

    def test_valeurs_negatives(self):
        # Teste des valeurs mesurées négatives.
        # Ces valeurs sont physiquement impossibles.
        trajet = TrajetObserve("F5", ["A", "B"], -5, -10)

        analyseur = AnalyseurTrajets(self.reseau, [trajet])
        analyseur.parcours = ParcoursReseau(self.reseau)

        anomalies = analyseur.detection_anomalies()

        # Vérifie que l’anomalie est correctement détectée
        self.assertTrue(
            any("Valeurs mesurées négatives" in a for a in anomalies["F5"]["FORMAT"])
        )

    def test_distance_sans_temps(self):
        # Teste le cas d’une distance positive avec un temps nul.
        # Cette situation viole les contraintes physiques élémentaires.
        trajet = TrajetObserve("F6", ["A", "B"], 0, 10)

        analyseur = AnalyseurTrajets(self.reseau, [trajet])
        analyseur.parcours = ParcoursReseau(self.reseau)

        anomalies = analyseur.detection_anomalies()

        # Vérifie que l’anomalie est bien classée en FORMAT
        self.assertTrue(
            any("Distance positive avec temps nul" in a for a in anomalies["F6"]["FORMAT"])
        )

    # ===============================
    # TESTS DES ANOMALIES LOGIQUES
    # ===============================

    def test_boucle(self):
        # Teste un trajet contenant une boucle (station répétée).
        # Cela indique un comportement anormal ou une incohérence.
        trajet = TrajetObserve("L1", ["A", "B", "A"], 20, 20)

        analyseur = AnalyseurTrajets(self.reseau, [trajet])
        analyseur.parcours = ParcoursReseau(self.reseau)

        anomalies = analyseur.detection_anomalies()

        # Vérifie que la boucle est bien détectée en anomalie LOGIQUE
        self.assertTrue(
            any("Boucle détectée" in a for a in anomalies["L1"]["LOGIQUE"])
        )

    def test_route_inexistante(self):
        # Teste un trajet empruntant une route absente du réseau.
        # Le trajet doit être marqué comme impossible théoriquement.
        trajet = TrajetObserve("L2", ["C", "A"], 20, 20)

        analyseur = AnalyseurTrajets(self.reseau, [trajet])
        analyseur.parcours = ParcoursReseau(self.reseau)

        anomalies = analyseur.detection_anomalies()

        # Vérifie la détection de la route inexistante
        self.assertTrue(
            any("Route inexistante" in a for a in anomalies["L2"]["LOGIQUE"])
        )

        # Vérifie que le trajet est jugé impossible
        self.assertTrue(
            any("Trajet théoriquement impossible" in a for a in anomalies["L2"]["LOGIQUE"])
        )

    # ===============================
    # TESTS DES ANOMALIES DE MESURE
    # ===============================

    def test_temps_trop_eleve(self):
        # Teste un temps mesuré largement supérieur au temps théorique.
        trajet = TrajetObserve("M1", ["A", "B", "C"], 100, 20)

        analyseur = AnalyseurTrajets(self.reseau, [trajet])
        analyseur.parcours = ParcoursReseau(self.reseau)

        anomalies = analyseur.detection_anomalies()

        # Vérifie la détection d’un temps mesuré trop élevé
        self.assertTrue(
            any("Temps mesuré trop élevé" in a for a in anomalies["M1"]["MESURE"])
        )

    def test_temps_trop_faible(self):
        # Teste un temps mesuré anormalement faible par rapport à la théorie.
        trajet = TrajetObserve("M2", ["A", "B", "C"], 5, 20)

        analyseur = AnalyseurTrajets(self.reseau, [trajet])
        analyseur.parcours = ParcoursReseau(self.reseau)

        anomalies = analyseur.detection_anomalies()

        # Vérifie la détection d’un temps mesuré trop faible
        self.assertTrue(
            any("Temps mesuré trop faible" in a for a in anomalies["M2"]["MESURE"])
        )

    def test_distance_trop_elevee(self):
        # Teste une distance mesurée trop grande par rapport à la distance théorique.
        trajet = TrajetObserve("M3", ["A", "B", "C"], 20, 100)

        analyseur = AnalyseurTrajets(self.reseau, [trajet])
        analyseur.parcours = ParcoursReseau(self.reseau)

        anomalies = analyseur.detection_anomalies()

        # Vérifie la détection d’une distance mesurée trop élevée
        self.assertTrue(
            any("Distance mesurée trop élevée" in a for a in anomalies["M3"]["MESURE"])
        )

    def test_distance_trop_faible(self):
        # Teste une distance mesurée trop faible par rapport à la distance théorique.
        trajet = TrajetObserve("M4", ["A", "B", "C"], 20, 5)

        analyseur = AnalyseurTrajets(self.reseau, [trajet])
        analyseur.parcours = ParcoursReseau(self.reseau)

        anomalies = analyseur.detection_anomalies()

        # Vérifie la détection d’une distance mesurée trop faible
        self.assertTrue(
            any("Distance mesurée trop faible" in a for a in anomalies["M4"]["MESURE"])
        )

    # ===============================
    # TESTS DU CALCUL THÉORIQUE
    # ===============================

    def test_calcul_theorie_valide(self):
        # Teste un trajet valide afin de vérifier le bon calcul
        # de la distance et du temps théoriques.
        trajet = TrajetObserve("TVAL", ["A", "B", "C"], 0, 0)

        analyseur = AnalyseurTrajets(self.reseau, [trajet])
        analyseur.parcours = ParcoursReseau(self.reseau)

        theorie = analyseur.calcul_theorie_trajet(trajet)

        self.assertEqual(theorie.distance_theorique, 20)
        self.assertEqual(theorie.temps_theorique, 20)
        self.assertEqual(theorie.segments_inexistants, [])

    def test_calcul_theorie_segment_inexistant(self):
        # Teste le calcul théorique lorsqu’un segment du trajet
        # n’existe pas dans le réseau.
        trajet = TrajetObserve("TINV", ["C", "A"], 0, 0)

        analyseur = AnalyseurTrajets(self.reseau, [trajet])
        analyseur.parcours = ParcoursReseau(self.reseau)

        theorie = analyseur.calcul_theorie_trajet(trajet)

        # Vérifie que le segment inexistant est correctement détecté
        self.assertIn(("C", "A"), theorie.segments_inexistants)


if __name__ == "__main__":
    unittest.main()
