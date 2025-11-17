from collections import deque   # obligatoire pour BFS

class ParcoursReseau:
    """
        Classe contenant les algorithmes de parcours BFS et DFS
        appliqués au réseau urbain.
    """


    def __init__(self, reseau):
        # Le réseau : instance de ReseauUrbain
        self.reseau = reseau


    def bfs(self, station_depart):
        """
                Parcours BFS à partir d'une station.
                Retourne l'ordre de visite.
        """
        if station_depart not in self.reseau.index_par_nom:  # Si la station de départ n'existe pas dans le réseau, on stoppe immédiatement
            raise ValueError("Station inconnue dans le réseau") # et on signale l'erreur pour éviter un parcours impossible.

        visites = []  # Pour enregistrer l'ordre des stations visitées
        file = deque()  # Pour stocker les stations a visité bientot file FIFO
        deja_vu = set()  # Pour ne jamais repasser sur une station déjà vue (sinon boucle infinie).

        file.append(station_depart)  # On place la station de départ dans la file
        deja_vu.add(station_depart)  # On marque la station comme déjà vue

        #Tant qu'il reste des éléments dans la liste

