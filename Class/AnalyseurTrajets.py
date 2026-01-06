from Class.Distance import Distance


class AnalyseurTrajets:
    def __init__(self, reseau, trajets_observes):
        self.reseau = reseau
        self.trajets_observes = trajets_observes

    def calcul_theorie_trajet(self, trajet):
        # Initialisation de la distance totale
        distance_totale = 0

        # Initialisation du temps total
        temps_total = 0

        # Liste des segments inexistants
        segments_inexistants = []

        # Liste des stations du trajet
        stations = trajet.stations_noms

        # Parcours des segments du trajet
        for i in range(len(stations) - 1):
            # Station de départ
            depart = stations[i]

            # Station d’arrivée
            arrivee = stations[i + 1]

            # Parcours DFS depuis la station de départ
            stations_accessibles = self.parcours.dfs(depart)

            # Si la station d’arrivée n’est pas atteignable → segment inexistant
            if arrivee not in stations_accessibles:
                segments_inexistants.append((depart, arrivee))
                continue

            # Récupération des index dans les matrices
            i_dep = self.reseau.index_par_nom[depart]
            i_arr = self.reseau.index_par_nom[arrivee]

            # Lecture des valeurs théoriques
            dist = self.reseau.matrice_distances[i_dep][i_arr]
            temps = self.reseau.matrice_temps[i_dep][i_arr]

            # Vérification finale de l’existence du segment
            if dist == -1 or temps == -1:
                segments_inexistants.append((depart, arrivee))
            else:
                distance_totale += dist
                temps_total += temps

        # Retourne un objet Distance (et plus un dictionnaire)
        return Distance(distance_totale, temps_total, segments_inexistants)

    def calcul_theorie_tous_trajets(self):
        resultats = []

        for trajet in self.trajets_observes:
            resultat = self.calcul_theorie_trajet(trajet)
            resultats.append((trajet.id_trajet, resultat))

        return resultats

    def detection_anomalies(self):
        anomalies = []  # liste qui contiendra toutes les anomalies détectées

        for trajet in self.trajets_observes:  # on parcourt tous les trajets observés
            stations = trajet.stations_noms  # récupération de la liste des stations du trajet

            if len(stations) != len(set(stations)):  # comparaison pour savoir si une station apparaît plusieurs fois
                anomalies.append(f"Boucle détectée dans le trajet {trajet.id_trajet}")  # ajout de l'anomalie

            theorie = self.calcul_theorie_trajet(trajet)  # calcul des valeurs théoriques du trajet

            for depart, arrivee in theorie["segments_inexistants"]:  # parcours des segments inexistants détectés
                anomalies.append(
                    f"Route manquante entre {depart} et {arrivee} (trajet {trajet.id_trajet})"
                )  # signalement d'une route manquante

            temps_theorique = theorie["temps_theorique"]  # récupération du temps théorique total
            if temps_theorique > 0:  # vérification pour éviter une division ou comparaison inutile
                if trajet.temps_mesure > 1.3 * temps_theorique:  # seuil de 30 % au-dessus du théorique
                    anomalies.append(
                        f"Temps mesuré incohérent pour le trajet {trajet.id_trajet}"
                    )  # ajout de l'anomalie de temps

            distance_theorique = theorie["distance_theorique"]  # récupération de la distance théorique
            if distance_theorique > 0:  # vérification que la distance existe
                if trajet.distance_mesuree > 1.3 * distance_theorique:  # même seuil que pour le temps
                    anomalies.append(
                        f"Distance mesurée incohérente pour le trajet {trajet.id_trajet}"
                    )  # ajout de l'anomalie de distance

            if len(theorie["segments_inexistants"]) > 0:  # si au moins un segment est inexistant
                anomalies.append(
                    f"Trajet {trajet.id_trajet} impossible théoriquement"
                )  # le trajet est considéré comme impossible

        return anomalies  # retour de la liste complète des anomalies
