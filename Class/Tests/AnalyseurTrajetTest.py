import unittest

from Class.AnalyseurTrajets import AnalyseurTrajets
from Class.TrajetObserve import TrajetObserve
from Class.ReseauUrbain import ReseauUrbain
from Class.ParcoursReseau import ParcoursReseau


class AnalyseurTrajetTest(unittest.TestCase):
    """
    Tests unitaires complets de la classe AnalyseurTrajets.

    Chaque test est volontairement ciblé sur UNE anomalie précise
    afin de vérifier que :
    - l’anomalie est correctement détectée
    - elle est classée dans la bonne catégorie (FORMAT, LOGIQUE, MESURE)
    """

    def setUp(self):
        # Création d’un réseau minimal mais cohérent,
        # commun à l’ensemble des tests unitaires.
        # A ---10---> B ---10---> C
        self.reseau = ReseauUrbain("reseau_test")

        self.reseau.ajouter_station("A")
        self.reseau.ajouter_station("B")
        self.reseau.ajouter_station("C")

        self.reseau.ajouter_route("A", "B", 10, 10)
        self.reseau.ajouter_route("B", "C", 10, 10)

    # ===============================
    # TESTS DES ANOMALIES DE FORMAT
    # ===============================

    def test_colonne_csv_manquante(self):
        """
        Vérifie la détection d’une colonne obligatoire manquante dans le CSV.

        On simule volontairement un objet trajet incomplet,
        auquel il manque l’attribut 'distMesure'.
        Ce cas correspond à un CSV mal structuré.
        """

        class TrajetIncomplet:
            def __init__(self):
                self.idTraj = "F0"
                self.nomsStations = ["A", "B"]
                self.tpsMesure = 10
                # distMesure est volontairement absent

        trajet = TrajetIncomplet()

        analyseur = AnalyseurTrajets(self.reseau, [trajet])
        analyseur.parcours = ParcoursReseau(self.reseau)

        anomalies = analyseur.detection_anomalies()

        # Vérifie que l’anomalie de colonne manquante est détectée
        self.assertTrue(
            any("Colonne CSV manquante" in a for a in anomalies["F0"]["FORMAT"])
        )

    def test_aucune_station(self):
        """
        Vérifie le cas d’un trajet sans aucune station.
        Cela correspond typiquement à une ligne vide dans le CSV.
        """

        trajet = TrajetObserve("F1", [], 10, 10)

        analyseur = AnalyseurTrajets(self.reseau, [trajet])
        analyseur.parcours = ParcoursReseau(self.reseau)

        anomalies = analyseur.detection_anomalies()

        # Le trajet doit être rejeté comme invalide
        self.assertIn("Aucune station renseignée", anomalies["F1"]["FORMAT"][0])

    def test_une_seule_station(self):
        """
        Vérifie le cas d’un trajet contenant une seule station.
        Un tel trajet ne représente aucun déplacement réel.
        """

        trajet = TrajetObserve("F2", ["A"], 10, 10)

        analyseur = AnalyseurTrajets(self.reseau, [trajet])
        analyseur.parcours = ParcoursReseau(self.reseau)

        anomalies = analyseur.detection_anomalies()

        # Vérifie que l’anomalie est correctement détectée
        self.assertTrue(
            any("Une seule station" in a for a in anomalies["F2"]["FORMAT"])
        )

    def test_station_inconnue(self):
        """
        Vérifie la détection d’une station absente du réseau.
        Cela simule une faute de frappe ou une incohérence de référentiel.
        """

        trajet = TrajetObserve("F3", ["A", "D"], 10, 10)

        analyseur = AnalyseurTrajets(self.reseau, [trajet])
        analyseur.parcours = ParcoursReseau(self.reseau)

        anomalies = analyseur.detection_anomalies()

        # La station inconnue doit être signalée
        self.assertTrue(
            any("Station inconnue" in a for a in anomalies["F3"]["FORMAT"])
        )

    def test_valeurs_manquantes(self):
        """
        Vérifie le cas où une valeur mesurée est absente (temps ou distance).
        Sans ces valeurs, la comparaison avec la théorie est impossible.
        """

        trajet = TrajetObserve("F4", ["A", "B"], None, 10)

        analyseur = AnalyseurTrajets(self.reseau, [trajet])
        analyseur.parcours = ParcoursReseau(self.reseau)

        anomalies = analyseur.detection_anomalies()

        self.assertTrue(
            any("Valeurs mesurées manquantes" in a for a in anomalies["F4"]["FORMAT"])
        )

    def test_valeurs_negatives(self):
        """
        Vérifie la détection de valeurs négatives pour le temps ou la distance.
        Ces valeurs sont physiquement impossibles.
        """

        trajet = TrajetObserve("F5", ["A", "B"], -5, -10)

        analyseur = AnalyseurTrajets(self.reseau, [trajet])
        analyseur.parcours = ParcoursReseau(self.reseau)

        anomalies = analyseur.detection_anomalies()

        self.assertTrue(
            any("Valeurs mesurées négatives" in a for a in anomalies["F5"]["FORMAT"])
        )

    def test_distance_sans_temps(self):
        """
        Vérifie le cas où une distance est fournie avec un temps nul.
        Cela viole les lois physiques élémentaires.
        """

        trajet = TrajetObserve("F6", ["A", "B"], 0, 10)

        analyseur = AnalyseurTrajets(self.reseau, [trajet])
        analyseur.parcours = ParcoursReseau(self.reseau)

        anomalies = analyseur.detection_anomalies()

        self.assertTrue(
            any("Distance positive avec temps nul" in a for a in anomalies["F6"]["FORMAT"])
        )

    # ===============================
    # TESTS DES ANOMALIES LOGIQUES
    # ===============================

    def test_boucle(self):
        """
        Vérifie la détection d’une boucle dans le trajet.
        Une station répétée indique un comportement incohérent.
        """

        trajet = TrajetObserve("L1", ["A", "B", "A"], 20, 20)

        analyseur = AnalyseurTrajets(self.reseau, [trajet])
        analyseur.parcours = ParcoursReseau(self.reseau)

        anomalies = analyseur.detection_anomalies()

        self.assertTrue(
            any("Boucle détectée" in a for a in anomalies["L1"]["LOGIQUE"])
        )

    def test_route_inexistante(self):
        """
        Vérifie la détection d’un trajet utilisant une route absente du réseau.
        Le trajet doit être déclaré impossible théoriquement.
        """

        trajet = TrajetObserve("L2", ["C", "A"], 20, 20)

        analyseur = AnalyseurTrajets(self.reseau, [trajet])
        analyseur.parcours = ParcoursReseau(self.reseau)

        anomalies = analyseur.detection_anomalies()

        self.assertTrue(
            any("Route inexistante" in a for a in anomalies["L2"]["LOGIQUE"])
        )
        self.assertTrue(
            any("Trajet théoriquement impossible" in a for a in anomalies["L2"]["LOGIQUE"])
        )

    # ===============================
    # TESTS DES ANOMALIES DE MESURE
    # ===============================

    def test_temps_trop_eleve(self):
        """
        Vérifie la détection d’un temps mesuré largement supérieur
        au temps théorique attendu.
        """

        trajet = TrajetObserve("M1", ["A", "B", "C"], 100, 20)

        analyseur = AnalyseurTrajets(self.reseau, [trajet])
        analyseur.parcours = ParcoursReseau(self.reseau)

        anomalies = analyseur.detection_anomalies()

        self.assertTrue(
            any("Temps mesuré trop élevé" in a for a in anomalies["M1"]["MESURE"])
        )

    def test_temps_trop_faible(self):
        """
        Vérifie la détection d’un temps mesuré anormalement faible
        par rapport au temps théorique.
        """

        trajet = TrajetObserve("M2", ["A", "B", "C"], 5, 20)

        analyseur = AnalyseurTrajets(self.reseau, [trajet])
        analyseur.parcours = ParcoursReseau(self.reseau)

        anomalies = analyseur.detection_anomalies()

        self.assertTrue(
            any("Temps mesuré trop faible" in a for a in anomalies["M2"]["MESURE"])
        )

    def test_distance_trop_elevee(self):
        """
        Vérifie la détection d’une distance mesurée trop grande
        par rapport à la distance théorique.
        """

        trajet = TrajetObserve("M3", ["A", "B", "C"], 20, 100)

        analyseur = AnalyseurTrajets(self.reseau, [trajet])
        analyseur.parcours = ParcoursReseau(self.reseau)

        anomalies = analyseur.detection_anomalies()

        self.assertTrue(
            any("Distance mesurée trop élevée" in a for a in anomalies["M3"]["MESURE"])
        )

    def test_distance_trop_faible(self):
        """
        Vérifie la détection d’une distance mesurée trop faible
        par rapport à la distance théorique.
        """

        trajet = TrajetObserve("M4", ["A", "B", "C"], 20, 5)

        analyseur = AnalyseurTrajets(self.reseau, [trajet])
        analyseur.parcours = ParcoursReseau(self.reseau)

        anomalies = analyseur.detection_anomalies()

        self.assertTrue(
            any("Distance mesurée trop faible" in a for a in anomalies["M4"]["MESURE"])
        )

    # ===============================
    # TESTS DU CALCUL THÉORIQUE
    # ===============================

    def test_calcul_theorie_valide(self):
        """
        Vérifie que le calcul théorique est correct
        pour un trajet valide du réseau.
        """

        trajet = TrajetObserve("TVAL", ["A", "B", "C"], 0, 0)

        analyseur = AnalyseurTrajets(self.reseau, [trajet])
        analyseur.parcours = ParcoursReseau(self.reseau)

        theorie = analyseur.calcul_theorie_trajet(trajet)

        self.assertEqual(theorie.distance_theorique, 20)
        self.assertEqual(theorie.temps_theorique, 20)
        self.assertEqual(theorie.segments_inexistants, [])

    def test_calcul_theorie_segment_inexistant(self):
        """
        Vérifie que le calcul théorique détecte correctement
        un segment absent du réseau.
        """

        trajet = TrajetObserve("TINV", ["C", "A"], 0, 0)

        analyseur = AnalyseurTrajets(self.reseau, [trajet])
        analyseur.parcours = ParcoursReseau(self.reseau)

        theorie = analyseur.calcul_theorie_trajet(trajet)

        self.assertIn(("C", "A"), theorie.segments_inexistants)


if __name__ == "__main__":
    unittest.main()
