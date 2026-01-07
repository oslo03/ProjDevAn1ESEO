from Class.Distance import Distance


class AnalyseurTrajets:
    def __init__(self, reseau, trajets_observes):
        self.reseau = reseau
        self.trajets_observes = trajets_observes

    def calcul_theorie_trajet(self, trajet):
        distance_totale = 0
        temps_total = 0
        segments_inexistants = []


        stations = trajet.nomsStations

        for i in range(len(stations) - 1):
            depart = stations[i]
            arrivee = stations[i + 1]

            i_dep = self.reseau.index_par_nom[depart]
            i_arr = self.reseau.index_par_nom[arrivee]

            dist = self.reseau.matrice_distances[i_dep][i_arr]
            temps = self.reseau.matrice_temps[i_dep][i_arr]

            if dist == -1 or temps == -1:
                segments_inexistants.append((depart, arrivee))
            else:
                distance_totale += dist
                temps_total += temps

        return Distance(distance_totale, temps_total, segments_inexistants)

    def calcul_theorie_tous_trajets(self):
        resultats = []

        for trajet in self.trajets_observes:
            resultat = self.calcul_theorie_trajet(trajet)
            resultats.append((trajet.idTraj, resultat))

        return resultats

    def detection_anomalies(self):
        anomalies = []

        for trajet in self.trajets_observes:
            stations = trajet.nomsStations  # ✅ bon attribut

            if len(stations) != len(set(stations)):
                anomalies.append(
                    f"Boucle détectée dans le trajet {trajet.idTraj}"
                )

            theorie = self.calcul_theorie_trajet(trajet)

            for depart, arrivee in theorie.segments_inexistants:
                anomalies.append(
                    f"Route manquante entre {depart} et {arrivee} (trajet {trajet.idTraj})"
                )

            if theorie.temps_theorique > 0:
                if trajet.tpsMesure > 1.3 * theorie.temps_theorique:
                    anomalies.append(
                        f"Temps mesuré incohérent pour le trajet {trajet.idTraj}"
                    )

            if theorie.distance_theorique > 0:
                if trajet.distMesure > 1.3 * theorie.distance_theorique:
                    anomalies.append(
                        f"Distance mesurée incohérente pour le trajet {trajet.idTraj}"
                    )

            if len(theorie.segments_inexistants) > 0:
                anomalies.append(
                    f"Trajet {trajet.idTraj} impossible théoriquement"
                )

        return anomalies
