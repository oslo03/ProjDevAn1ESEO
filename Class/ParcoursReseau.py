from collections import deque          # Import de deque, une file très efficace pour BFS
from Class.ReseauUrbain import ReseauUrbain   # Import de la classe ReseauUrbain

class ParcoursReseau:
    """
        Classe contenant les algorithmes de parcours BFS et DFS
        appliqués au réseau urbain.
    """

    def __init__(self, reseau):
        self.reseau = reseau           # On garde une référence au réseau à parcourir

    # ---------------------------------------------------------
    # Trouver l’id d’une station à partir de son nom
    # ---------------------------------------------------------
    def _get_station_id(self, nom):
        for station in self.reseau.stations:   # On parcourt toutes les stations du réseau
            if station.nom == nom:             # Si on trouve celle dont le nom correspond
                return station.id              # On renvoie son identifiant interne
        return None                             # Sinon on renvoie None

    # ---------------------------------------------------------
    # Obtenir les voisins d’une station (noms), en lisant timeMat
    # ---------------------------------------------------------
    def _voisins(self, nom_station):
        id_dep = self._get_station_id(nom_station)   # Récupère l'id de la station de départ
        if id_dep is None:                           # Si la station n'existe pas
            return []                                # Aucune liste de voisins possible

        voisins = []                                  # Liste des voisins à renvoyer

        # timeMat[id_dep] = liste des durées vers toutes les autres stations
        for id_end, duree in enumerate(self.reseau.timeMat[id_dep]):
            if duree is not None:                    # Si une durée existe, une route existe
                voisins.append(self.reseau.stations[id_end].nom)  # On ajoute le nom du voisin

        return voisins                                # Renvoie la liste des voisins

    # ---------------------------------------------------------
    # BFS (parcours en largeur)
    # ---------------------------------------------------------
    def bfs(self, station_depart):
        # Vérifie que la station existe dans le réseau
        if self._get_station_id(station_depart) is None:
            raise ValueError("Station inconnue dans le réseau")

        visites = []                    # Liste de stations dans l'ordre de visite
        file = deque()                  # File FIFO pour le BFS
        deja_vu = set()                 # Ensemble des stations déjà visitées

        file.append(station_depart)     # On met la station de départ dans la file
        deja_vu.add(station_depart)     # On la marque comme visitée

        # Tant que la file n'est pas vide
        while file:
            station_courante = file.popleft()   # On retire la station en tête de file
            visites.append(station_courante)    # On l'ajoute à la liste des visites

            # On parcourt tous les voisins accessibles
            for voisin in self._voisins(station_courante):
                if voisin not in deja_vu:       # Si le voisin n'a jamais été visité
                    deja_vu.add(voisin)         # On le marque comme visité
                    file.append(voisin)         # On l'ajoute dans la file pour traitement

        return visites                           # On renvoie la liste complète du parcours BFS


# ============================================================
# Test du BFS (se lance uniquement si ce fichier est exécuté directement)
# ============================================================
if __name__ == "__main__":
    from ReseauUrbain import ReseauUrbain   # On réimporte pour lancer le test

    r = ReseauUrbain("Test")               # Création d’un réseau nommé "Test"

    # Stations (ajoutées dans le réseau)
    r.addStation("A")
    r.addStation("B")
    r.addStation("C")
    r.addStation("D")

    # Routes entre stations (durée, distance)
    r.addRoad("A", "B", 1, 1)
    r.addRoad("A", "C", 1, 1)
    r.addRoad("B", "D", 1, 1)
    r.addRoad("C", "D", 1, 1)

    parcours = ParcoursReseau(r)           # Création du module de parcours
    print("BFS depuis A :", parcours.bfs("A"))   # Lancement du BFS depuis "A"
