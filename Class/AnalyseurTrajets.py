class AnalyseurTrajets:
    def __init__(self, reseau, trajets_observes):
        self.reseau = reseau
        self.trajets_observes = trajets_observes

    def calcul_theorie_trajet(self, trajet):
        distance_totale = 0
        temps_total = 0
        segments_inexistants = []

        stations = trajet.stations_noms

        for i in range(len(stations) - 1):
            depart = stations[i]
            arrivee = stations[i + 1]

            if depart not in self.reseau.index_par_nom or arrivee not in self.reseau.index_par_nom:
                segments_inexistants.append((depart, arrivee))
                continue

            i_dep = self.reseau.index_par_nom[depart]
            i_arr = self.reseau.index_par_nom[arrivee]

            dist = self.reseau.matrice_distances[i_dep][i_arr]
            temps = self.reseau.matrice_temps[i_dep][i_arr]

            if dist == -1 or temps == -1:
                segments_inexistants.append((depart, arrivee))
            else:
                distance_totale += dist
                temps_total += temps

        return {
            "distance_theorique": distance_totale,
            "temps_theorique": temps_total,
            "segments_inexistants": segments_inexistants
        }

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
