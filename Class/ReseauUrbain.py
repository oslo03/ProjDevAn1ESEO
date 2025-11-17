from Class.Station import Station

class ReseauUrbain:
    def __init__(self, nom):
        self.nom = nom
        self.stations = []  # liste d'objets Station
        self.timeMat = []   # matrice de durées
        self.distMat = []   # matrice de distances

    def addStation(self, nomStation):
        """
        Ajoute une station et met à jour les matrices NxN
        """
        new_id = len(self.stations)
        station = Station(new_id, nomStation)
        self.stations.append(station)

        self._resizeMatrices()

        return station

    def _resizeMatrices(self):
        n = len(self.stations)

        # Ajouter une colonne à chaque ligne existante
        for row in self.timeMat:
            row.append(None)
        for row in self.distMat:
            row.append(None)

        # Ajouter une nouvelle ligne pour la nouvelle station
        self.timeMat.append([None] * n)
        self.distMat.append([None] * n)

    def addRoad(self, depName, endName, duration, dist):
        #trouve la station dont le nom correspond à depName sinon None, par defaut récupère le premier élément du générateur
        # La fonction next() renvoie l’élément suivant de l’itérateur.
        dep = next((s for s in self.stations if s.nom == depName), None)
        end = next((s for s in self.stations if s.nom == endName), None)

        if dep is None or end is None:
            raise ValueError(f"Station introuvable : {depName} ou {endName}")

        self.timeMat[dep.id][end.id] = duration
        self.distMat[dep.id][end.id] = dist

    def __str__(self):
        return f"Réseau {self.nom} avec {len(self.stations)} stations"


    def neighbours(self):
        return "Station "+str(self.nom)+" ID: "+str(self.id)

    def initMatrices(self):
        return "Station "+str(self.nom)+" ID: "+str(self.id)

    def affichage(self):
        return "Station "+str(self.nom)+" ID: "+str(self.id)

    def __str__(self):
        return f"Réseau {self.nom} avec {len(self.stations)} stations"
