from Station import Station

class ReseauUrbain:
    id = 1
    def __init__(self, nom, nomStation):
        self.nom = nom
        self.obj = Station(ReseauUrbain.id, nomStation)
        self.timeMat = [[]]
        self.timeMat = [[]]
        ReseauUrbain.id += 1

    def addStation(self, addedStation):
        return "Station "+str(self.nom)+" ID: "+str(self.id)

    def addRoad(self, addedRoad):
        return "Station "+str(self.nom)+" ID: "+str(self.id)

    def neighbours(self):
        return "Station "+str(self.nom)+" ID: "+str(self.id)

    def initMatrices(self):
        return "Station "+str(self.nom)+" ID: "+str(self.id)

    def affichage(self):
        return "Station "+str(self.nom)+" ID: "+str(self.id)

    def __str__ (self):
        return "Station " + str(self.nom) + " ID: " + str(self.id)

#main de test
if __name__ == '__main__':
    villeTest1=Station(1, "Franc-Bourgogne")
    print(villeTest1.affichage())
    print(str(villeTest1))