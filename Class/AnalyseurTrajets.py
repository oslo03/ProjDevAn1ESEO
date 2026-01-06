import TrajetObserve as trjObs

#Classe de trajet observée, avec la liste des stations parcourus et la meusure de temps et de distance.

class AnalyseurTrajets:
    # Classe contenant differante méthode pour analyser les différents trajet..
    # Contient TODO
    def __init__(self, reseau, trajObserve):
        self.reseau=reseau
        self.trajObserve=trajObserve

    def calcTrajetTheorique(self, trajet):
        return False

    def compTheorieMesuree(self, Theorique, Observe):
        return Observe - Theorique

    def detectAnomalie(self):
        return False

    def interpretAnomalie(self):
        return False

