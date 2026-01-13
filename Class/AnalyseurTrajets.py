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
    # Au-delà, la mesure est considérée comme suspecte
    MAX_RATIO = 1.3

    # Tolérance maximale en dessous de la valeur théorique (-30 %)
    # En dessous, la mesure est considérée comme anormalement faible
    MIN_RATIO = 0.7

    def __init__(self, reseau, trajets_observes):
        self.reseau = reseau
        self.trajets_observes = trajets_observes

    def calcul_theorie_trajet(self, trajet):
        """
        Calcule la distance et le temps théoriques d’un trajet
        en se basant sur les matrices du réseau.

        Cette méthode permet également d’identifier les segments
        inexistants entre deux stations consécutives.
        """

        distance_totale = 0
        temps_total = 0
        segments_inexistants = []

        stations = trajet.nomsStations

        for i in range(len(stations) - 1):
            depart = stations[i]
            arrivee = stations[i + 1]

            # Vérifie, via un parcours en profondeur (DFS),
            # si la station d’arrivée est atteignable depuis la station de départ
            stations_atteignables = self.parcours.dfs(depart)

            # Si l’arrivée n’est pas atteignable, le segment est inexistant
            # Le calcul théorique ne peut pas continuer sur ce segment
            if arrivee not in stations_atteignables:
                segments_inexistants.append((depart, arrivee))
                continue

            # Accès aux indices des stations dans les matrices du réseau
            i_dep = self.reseau.index_par_nom[depart]
            i_arr = self.reseau.index_par_nom[arrivee]

            dist = self.reseau.matrice_distances[i_dep][i_arr]
            temps = self.reseau.matrice_temps[i_dep][i_arr]

            # Une valeur négative indique une liaison absente ou invalide
            if dist < 0 or temps < 0:
                segments_inexistants.append((depart, arrivee))
            else:
                distance_totale += dist
                temps_total += temps

        return Distance(distance_totale, temps_total, segments_inexistants)

    def calcul_theorie_tous_trajets(self):
        """
        Calcule les valeurs théoriques pour l’ensemble des trajets observés.
        """
        resultats = []

        for trajet in self.trajets_observes:
            resultat = self.calcul_theorie_trajet(trajet)
            resultats.append((trajet.idTraj, resultat))

        return resultats

    # Retourne la différence entre le temps de trajet mesuré
    # et le temps théorique, exprimée en pourcentage
    def comparaison_theorie_mesure(self, tpsTheorie, tpsMesure):
        return (tpsMesure * 100) / tpsTheorie

    def detection_anomalies(self):
        """
        Détecte l’ensemble des anomalies pour chaque trajet observé.

        Les anomalies sont classées par niveau de gravité :
        - ALERTE    : erreur critique rendant le trajet invalide ou inutilisable
        - ATTENTION : incohérence importante nécessitant une vérification
        - NOTICE    : anomalie mineure ou informative
        """

        anomalies = {}

        for trajet in self.trajets_observes:
            # Récupération sécurisée de l’identifiant du trajet
            traj_id = getattr(trajet, "idTraj", "INCONNU")

            anomalies[traj_id] = {
                "FORMAT": [],
                "LOGIQUE": [],
                "MESURE": []
            }

            # ======================================================
            # FORMAT — VÉRIFICATION DES COLONNES CSV
            # ======================================================

            # Liste des colonnes obligatoires attendues dans le CSV.
            # Leur absence indique un problème structurel du fichier.
            colonnes_attendues = [
                "idTraj",
                "nomsStations",
                "tpsMesure",
                "distMesure"
            ]

            # Vérifie que chaque colonne attendue est bien présente
            # dans l’objet trajet issu du CSV
            for colonne in colonnes_attendues:
                if not hasattr(trajet, colonne):
                    anomalies[traj_id]["FORMAT"].append(
                        f"[ALERTE] Colonne CSV manquante : {colonne}"
                    )

            # Si une colonne obligatoire manque, le trajet est inutilisable
            # Il est inutile de poursuivre l’analyse
            if anomalies[traj_id]["FORMAT"]:
                continue

            stations = trajet.nomsStations

            # ======================================================
            # FORMAT — COHÉRENCE DES DONNÉES CSV
            # ======================================================

            # Aucun arrêt n’est renseigné : le trajet est vide
            if not stations or len(stations) == 0:
                anomalies[traj_id]["FORMAT"].append(
                    "[ALERTE] Aucune station renseignée dans le CSV"
                )
                continue

            # Une seule station ne correspond à aucun déplacement réel
            if len(stations) == 1:
                anomalies[traj_id]["FORMAT"].append(
                    "[ALERTE] Une seule station renseignée (trajet invalide)"
                )

            # Vérifie que chaque station du CSV existe bien dans le réseau
            for station in stations:
                if station not in self.reseau.index_par_nom:
                    anomalies[traj_id]["FORMAT"].append(
                        f"[ALERTE] Station inconnue dans le réseau : {station}"
                    )

            # Les valeurs mesurées sont indispensables pour toute comparaison
            if trajet.tpsMesure is None or trajet.distMesure is None:
                anomalies[traj_id]["FORMAT"].append(
                    "[ALERTE] Valeurs mesurées manquantes (temps ou distance)"
                )
                continue

            # Des valeurs négatives sont physiquement impossibles
            if trajet.tpsMesure < 0 or trajet.distMesure < 0:
                anomalies[traj_id]["FORMAT"].append(
                    "[ALERTE] Valeurs mesurées négatives"
                )

            # Une distance non nulle avec un temps nul est incohérente
            if trajet.distMesure > 0 and trajet.tpsMesure == 0:
                anomalies[traj_id]["FORMAT"].append(
                    "[ALERTE] Distance positive avec temps nul"
                )

            # ======================================================
            # LOGIQUE — COHÉRENCE DU TRAJET
            # ======================================================

            # La répétition d’une station indique une boucle
            # Cela peut être une erreur de données ou un comportement anormal
            if len(stations) != len(set(stations)):
                anomalies[traj_id]["LOGIQUE"].append(
                    "[ATTENTION] Boucle détectée (station répétée)"
                )

            theorie = self.calcul_theorie_trajet(trajet)

            # Chaque segment inexistant correspond à une rupture du réseau
            for depart, arrivee in theorie.segments_inexistants:
                anomalies[traj_id]["LOGIQUE"].append(
                    f"[ALERTE] Route inexistante entre {depart} et {arrivee}"
                )

            # Si au moins un segment est impossible,
            # le trajet entier est irréalisable théoriquement
            if len(theorie.segments_inexistants) > 0:
                anomalies[traj_id]["LOGIQUE"].append(
                    "[ALERTE] Trajet théoriquement impossible"
                )

            # ======================================================
            # MESURE — COMPARAISON MESURÉ / THÉORIQUE
            # ======================================================

            # Un temps trop élevé peut indiquer une erreur de mesure
            # ou un événement anormal durant le trajet
            if theorie.temps_theorique > 0:
                if trajet.tpsMesure > self.MAX_RATIO * theorie.temps_theorique:
                    anomalies[traj_id]["MESURE"].append(
                        "[ATTENTION] Temps mesuré trop élevé par rapport à la théorie"
                    )

                # Un temps trop faible est souvent informatif
                # (erreur d’arrondi, données approximatives)
                elif trajet.tpsMesure < self.MIN_RATIO * theorie.temps_theorique:
                    anomalies[traj_id]["MESURE"].append(
                        "[NOTICE] Temps mesuré trop faible par rapport à la théorie"
                    )

            # Même logique pour la distance mesurée
            if theorie.distance_theorique > 0:
                if trajet.distMesure > self.MAX_RATIO * theorie.distance_theorique:
                    anomalies[traj_id]["MESURE"].append(
                        "[ATTENTION] Distance mesurée trop élevée par rapport à la théorie"
                    )
                elif trajet.distMesure < self.MIN_RATIO * theorie.distance_theorique:
                    anomalies[traj_id]["MESURE"].append(
                        "[NOTICE] Distance mesurée trop faible par rapport à la théorie"
                    )

        return anomalies

if __name__ == "__main__":
    analyseur=AnalyseurTrajets(None, None)
    print("BLABLABLA:")
    print("Temps theorique depassant le temps mesure:")
    print(str(analyseur.comparaison_theorie_mesure(50, 65))+"%")
    print("Temps mesure depassant le temps theorique:")
    print(str(analyseur.comparaison_theorie_mesure(65, 50))+"%")