from Class.Distance import Distance


class AnalyseurTrajets:
    """
    Cette classe analyse des trajets observés (issus d’un CSV)
    et détecte des anomalies en comparant :
    - les données mesurées (temps, distance)
    - les valeurs théoriques calculées à partir du réseau
    """

    # ===============================
    # Constantes de seuils
    # ===============================

    # Tolérance maximale au-dessus de la valeur théorique (+30 %)
    MAX_RATIO = 1.3

    # Tolérance maximale en dessous de la valeur théorique (-30 %)
    MIN_RATIO = 0.7

    def __init__(self, reseau, trajets_observes):
        self.reseau = reseau
        self.trajets_observes = trajets_observes

    def calcul_theorie_trajet(self, trajet):
        """
        Calcule la distance et le temps théoriques d’un trajet
        en se basant sur les matrices du réseau.
        Détecte également les segments inexistants.
        """

        distance_totale = 0
        temps_total = 0
        segments_inexistants = []

        stations = trajet.nomsStations

        for i in range(len(stations) - 1):
            depart = stations[i]
            arrivee = stations[i + 1]

            # Utilisation d’un DFS pour vérifier si la station d’arrivée
            # est atteignable depuis la station de départ
            stations_atteignables = self.parcours.dfs(depart)

            # Si la station d’arrivée n’est pas atteignable,
            # le segment est considéré comme inexistant
            if arrivee not in stations_atteignables:
                segments_inexistants.append((depart, arrivee))
                continue

            # Accès aux matrices uniquement après validation du DFS
            i_dep = self.reseau.index_par_nom[depart]
            i_arr = self.reseau.index_par_nom[arrivee]

            dist = self.reseau.matrice_distances[i_dep][i_arr]
            temps = self.reseau.matrice_temps[i_dep][i_arr]

            # Une valeur négative indique une liaison invalide ou absente
            if dist < 0 or temps < 0:
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

    #TODO remettre fonction calcul différence tps theorique/concret (en %)

    #Retourne la différence entre le temps de trajet mesuré et celui observé (en pourcentage.)
    def comparaison_theorie_mesure(self, tpsTheorie, tpsMesure):
        return (tpsMesure*100)/tpsTheorie

    def detection_anomalies(self):
        """
        Détecte l’ensemble des anomalies pour chaque trajet observé.

        Le résultat est un dictionnaire structuré afin de :
        - regrouper les anomalies par trajet
        - distinguer clairement les différents types d’anomalies
        - faciliter l’analyse, l’affichage et les traitements futurs
        """

        # Dictionnaire principal des anomalies
        # Clé   : identifiant du trajet (idTraj)
        # Valeur: dictionnaire contenant les anomalies de ce trajet
        anomalies = {}

        for trajet in self.trajets_observes:
            traj_id = trajet.idTraj
            stations = trajet.nomsStations

            # Initialisation de la structure d’anomalies pour un trajet donné.
            # Chaque trajet possède son propre sous-dictionnaire,
            # ce qui permet d’isoler clairement les problèmes trajet par trajet.
            anomalies[traj_id] = {

                # Anomalies liées au format du CSV et aux données d’entrée.
                # On y place toutes les erreurs empêchant une analyse correcte.
                "FORMAT": [],

                # Anomalies liées à la logique du trajet ou au réseau.
                # Elles indiquent que le trajet est incohérent ou impossible.
                "LOGIQUE": [],

                # Anomalies liées à la comparaison entre mesures et théorie.
                # Elles signalent des écarts anormaux dans les données mesurées.
                "MESURE": []
            }

            # ======================================================
            # ANOMALIES DE FORMAT / DONNÉES CSV
            # ======================================================

            # Un trajet sans station est invalide.
            # Cela correspond généralement à une ligne vide ou corrompue dans le CSV.
            if not stations or len(stations) == 0:
                anomalies[traj_id]["FORMAT"].append(
                    "Aucune station renseignée dans le CSV"
                )
                continue

            # Un trajet avec une seule station ne représente aucun déplacement.
            # Il est donc incohérent d’un point de vue fonctionnel.
            if len(stations) == 1:
                anomalies[traj_id]["FORMAT"].append(
                    "Une seule station renseignée (trajet invalide)"
                )

            # Chaque station du CSV doit exister dans le réseau.
            # Une station inconnue indique une erreur de saisie ou de référentiel.
            for station in stations:
                if station not in self.reseau.index_par_nom:
                    anomalies[traj_id]["FORMAT"].append(
                        f"Station inconnue dans le réseau : {station}"
                    )

            # Les valeurs mesurées sont indispensables pour toute analyse.
            # Leur absence empêche toute comparaison avec la théorie.
            if trajet.tpsMesure is None or trajet.distMesure is None:
                anomalies[traj_id]["FORMAT"].append(
                    "Valeurs mesurées manquantes (temps ou distance)"
                )
                continue

            # Des valeurs négatives pour le temps ou la distance
            # sont physiquement impossibles.
            if trajet.tpsMesure < 0 or trajet.distMesure < 0:
                anomalies[traj_id]["FORMAT"].append(
                    "Valeurs mesurées négatives"
                )

            # Une distance strictement positive avec un temps nul
            # viole les contraintes physiques élémentaires.
            if trajet.distMesure > 0 and trajet.tpsMesure == 0:
                anomalies[traj_id]["FORMAT"].append(
                    "Distance positive avec temps nul"
                )

            # ======================================================
            # ANOMALIES LOGIQUES
            # ======================================================

            # La répétition d’une station indique une boucle dans le trajet.
            # Cela peut révéler un comportement anormal ou une erreur de données.
            if len(stations) != len(set(stations)):
                anomalies[traj_id]["LOGIQUE"].append(
                    "Boucle détectée (station répétée)"
                )

            theorie = self.calcul_theorie_trajet(trajet)

            # Chaque segment inexistant correspond à une liaison absente du réseau.
            for depart, arrivee in theorie.segments_inexistants:
                anomalies[traj_id]["LOGIQUE"].append(
                    f"Route inexistante entre {depart} et {arrivee}"
                )

            # Si au moins un segment est impossible,
            # alors le trajet entier est irréalisable théoriquement.
            if len(theorie.segments_inexistants) > 0:
                anomalies[traj_id]["LOGIQUE"].append(
                    "Trajet théoriquement impossible"
                )

            # ======================================================
            # COMPARAISON MESURÉ / THÉORIQUE
            # ======================================================

            # Comparaison du temps mesuré avec le temps théorique.
            # Un écart trop important suggère une anomalie de mesure ou de données.
            if theorie.temps_theorique > 0:
                if trajet.tpsMesure > self.MAX_RATIO * theorie.temps_theorique:
                    anomalies[traj_id]["MESURE"].append(
                        "Temps mesuré trop élevé par rapport à la théorie"
                    )
                elif trajet.tpsMesure < self.MIN_RATIO * theorie.temps_theorique:
                    anomalies[traj_id]["MESURE"].append(
                        "Temps mesuré trop faible par rapport à la théorie"
                    )

            # Comparaison de la distance mesurée avec la distance théorique.
            # Des écarts significatifs peuvent indiquer des erreurs GPS ou de saisie.
            if theorie.distance_theorique > 0:
                if trajet.distMesure > self.MAX_RATIO * theorie.distance_theorique:
                    anomalies[traj_id]["MESURE"].append(
                        "Distance mesurée trop élevée par rapport à la théorie"
                    )
                elif trajet.distMesure < self.MIN_RATIO * theorie.distance_theorique:
                    anomalies[traj_id]["MESURE"].append(
                        "Distance mesurée trop faible par rapport à la théorie"
                    )

        return anomalies
