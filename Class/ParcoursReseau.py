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
                Parcours BFS à partir d'une station. (BFS = Breadth-First Search)
                Retourne l'ordre de visite.
        """
        if station_depart not in self.reseau.index_par_nom:  # Si la station de départ n'existe pas dans le réseau, on stoppe immédiatement
            raise ValueError("Station inconnue dans le réseau") # et on signale l'erreur pour éviter un parcours impossible.

        visites = []  # Pour enregistrer l'ordre des stations visitées
        file = deque()  # Pour stocker les stations a visité bientôt file FIFO
        deja_vu = set()  # Pour ne jamais repasser sur une station déjà vue (sinon boucle infinie).

        file.append(station_depart)  # On place la station de départ dans la file
        deja_vu.add(station_depart)  # On marque la station comme déjà vue

        #Tant qu'il reste des éléments dans la liste
        while file:
            station_courante = file.popleft()  # On retire la station en tête de file (FIFO)
            visites.append(station_courante)  # On ajoute cette station dans l'ordre de visite

            # On parcourt tous les voisins accessibles depuis la station courante
            for voisin in self.reseau.voisins(station_courante):
                if voisin not in deja_vu:  # Si le voisin n'a pas déjà été visité
                    deja_vu.add(voisin)  # On le marque comme visité
                    file.append(voisin)  # On l'ajoute en fin de file pour le traiter plus tard

        return visites  # On renvoie l'ordre complet du parcours BFS


# ============================================================
# Test du bfs
# ============================================================
if __name__ == "__main__":
    from ReseauUrbain import ReseauUrbain   # On importe la classe réseau pour pouvoir tester

    r = ReseauUrbain()       # Création d’un réseau vide
    r.addRoad("A")   # Ajout de 4 stations
    r.addRoad("B")
    r.addRoad("C")
    r.addRoad("D")

    # Ajout de routes (liaisons) entre stations
    r.addRoad("A", "B", 1, 1)
    r.addRoad("A", "C", 1, 1)
    r.addRoad("B", "D", 1, 1)
    r.addRoad("C", "D", 1, 1)

    parcours = ParcoursReseau(r)   # On crée l’objet permettant d'utiliser BFS/DFS

    print("BFS depuis A :", parcours.bfs("A"))   # Test du BFS