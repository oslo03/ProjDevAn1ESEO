class Station:
    # Constructeur avec definition des attributs.
    def __init__(self, id, nom):
        self.id = id
        self.nom = nom

    #Fonction d'affichage, retourne un string.
    def affichage(self):
        return "Station "+str(self.nom)+" ID: "+str(self.id)

    #Redefinis le comportement de la classe quand on le convertie en string.
    def __str__ (self):
        return "Station " + str(self.nom) + " ID: " + str(self.id)