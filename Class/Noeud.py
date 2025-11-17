class Noeud:
    #Classe représentant un noeud d'une liste simplement chaînée.
    #Chaque noeud contient une valeur et un pointeur vers le noeud suivant.

    def __init__(self, valeur, suivant):
        self.valeur = valeur
        self.suivant = suivant

    @staticmethod
    def vide():
        #Crée un Noeud vide.
        #Retourne: Un Noeud avec une tête de valeur 0 et aucun reste.
        return Noeud(0, None)

    def est_vide(self):
        #Vérifie si le Noeud est vide.
        #Retourne: - True si le noeud est vide, False sinon.
        return self.valeur == 0

    def get_longueur(self):
        #Calcule la longeur de la liste Chainée.
        #Retourne: - Nombre entier représentant la taille de la liste.
        if self.est_vide():
            return 0
        return self.suivant.get_longueur()+1

    def affichage(self):
        #Génère une représentation en chaîne des éléments de la liste.
        #Retourne: - Une chaîne contenant les éléments séparés par des espaces.
        if self.est_vide():
            return ""
        if self.suivant.suivant==None:
            return str(self.valeur)
        return str(self.valeur) + " " + self.suivant.affichage()

    def ajoute_fin(self, nouvel_element):
        #Ajoute un nouvel élément au bout de la liste.
        #Paramètres: - nouvel_element : élément à ajouter.
        #Retourne: - Une nouvelle liste avec l'élément ajouté.
        if self.est_vide():
            return Noeud(nouvel_element, Noeud.vide())
        if self.suivant.suivant==None or self.suivant==None:
            nouveau_suivant = Noeud(nouvel_element, Noeud.vide())
            return Noeud(self.valeur, nouveau_suivant)
        return Noeud(self.valeur, self.suivant.ajoute_fin(nouvel_element))

    def ListeToString(self):
        # Génère une représentation en chaîne des éléments de la liste séparé par des ';' pour le traitement.
        # Retourne: - Une chaîne contenant les éléments séparés par des ';'.
        if self.est_vide():
            return ""
        if self.suivant.suivant==None:
            return str(self.valeur)
        return str(self.valeur) + ";" + self.suivant.ListeToString()

#main de test
if __name__ == "__main__":
    print("=== Test de la classe Noeud ===")

    #Les tests sont dans Liste Chainee

    print("=== Fin du test ===")
