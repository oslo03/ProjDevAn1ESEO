class AnalyseurTrajets:
    def __init__(self, reseau, trajets_observes):
        self.reseau = reseau
        self.trajets_observes = trajets_observes

    def calcul_theorie_trajet(self, trajet):
        distance_totale = 0
        temps_total = 0
        segments_inexistants = []

        stations = trajet.stations_noms

        for i in range(len(stations) - 1): #parcours les stations
            depart = stations[i] #station de depart
            arrivee = stations[i + 1] #station d'arrivee

            if depart not in self.reseau.index_par_nom or arrivee not in self.reseau.index_par_nom:
                segments_inexistants.append((depart, arrivee))
                continue

            i_dep = self.reseau.index_par_nom[depart] #index de station de départ
            i_arr = self.reseau.index_par_nom[arrivee] #index de station d'arrivee

            dist = self.reseau.matrice_distances[i_dep][i_arr] #distance de : station de départ x station d'arrivee
            temps = self.reseau.matrice_temps[i_dep][i_arr] # temps de ""

            if dist == -1 or temps == -1:
                segments_inexistants.append((depart, arrivee)) #segment prend la valeur de départ et d'arrivée
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
