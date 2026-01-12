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
    # Obtenir les voisins d’une station (noms)
    # ---------------------------------------------------------
    def _voisins(self, nom_station):
        # On délègue directement au réseau urbain
        return self.reseau.voisins(nom_station)

    # ---------------------------------------------------------
    # BFS (parcours en largeur)
    # ---------------------------------------------------------
    def bfs(self, station_depart):
        # Vérifie que la station existe dans le réseau
        if station_depart not in self.reseau.index_par_nom:
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
                    file.append(voisin)         # On l'ajoute dans la file

        return visites                           # On renvoie la liste complète du parcours BFS

    # ---------------------------------------------------------
    # DFS (parcours en profondeur)
    # ---------------------------------------------------------
    def dfs(self, station_depart):
        # Vérifie que la station existe
        if station_depart not in self.reseau.index_par_nom:
            raise ValueError("Station inconnue dans le réseau")

        visites = []         # Liste de l’ordre de visite
        pile = []            # Pile LIFO pour le DFS
        deja_vu = set()      # Ensemble des stations déjà visitées

        pile.append(station_depart)    # On empile la station de départ

        # Tant que la pile n'est pas vide
        while pile:
            station_courante = pile.pop()   # pop() = dernier entré → premier sorti

            if station_courante not in deja_vu:
                visites.append(station_courante)   # On visite la station
                deja_vu.add(station_courante)      # On la marque comme visitée

                # On récupère les voisins de la station courante
                # DFS cherche à aller en profondeur, donc on empile les voisins
                # On inverse la liste pour conserver un ordre logique
                voisins = self._voisins(station_courante)
                for voisin in reversed(voisins):
                    if voisin not in deja_vu:
                        pile.append(voisin)

        return visites                            # On renvoie la liste complète du parcours DFS

