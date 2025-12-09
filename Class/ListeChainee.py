#import Noeud
import unittest
from Class.Noeud import Noeud


class ListeChainee:

    # Classe représentant une liste chaînée de Noeud.
    # Contient une tete avec le premier Noeud de la liste et des fonction pour interagir avec la liste.

    def __init__(self, tete=None):
        #Initialise une liste avec une tête et un reste.
        #Tete: classe Noeud
        self.tete = tete

    def get_tete(self):
        #Retourne la valeur de la tête de la liste.
        return self.tete

    def set_tete(self, tete):
        #set l'attribut tete.
        self.tete = tete

    #La liste chainee est composée de noeud avec une entité ListeChainee devant.
    #par simplicité, les fonctions pour parcourir et intéragir avec la liste sont dans Noeud. Les fonctions suivantes permet de utiliser ceux du premier Noeud.

    def get_longueur(self):
        #Calcule la longeur de la liste Chainée.
        #Retourne: - Nombre entier représentant la taille de la liste.
        return self.tete.get_longueur()

    def affichage(self):
        #Génère une représentation en string des éléments de la liste.
        #Retourne: - Une string contenant les éléments séparés par des espaces.
        return self.tete.affichage()

    def ListeToString(self):
        #Génère une représentation en chaîne des éléments de la liste séparé par des ';' pour le traitement.
        #Retourne: - Une chaîne contenant les éléments séparés par des ';'.
        return self.tete.affichage()

    def ajoute_fin(self, nouvel_element):
        #Ajoute un nouvel élément au bout de la liste.

        #Paramètres: - nouvel_element : élément à ajouter.
        #Retourne: - Une nouvelle liste avec l'élément ajouté.

        return self.tete.ajoute_fin(nouvel_element)

    def parcourir(self):
        #retourne la liste chainé en liste Python.
        return self.tete.ListeToString().split(sep=";")

#Class de test
class TestListeChainee(unittest.TestCase):
    #listChain = ListeChainee(Noeud("Erasme", Noeud("CHU Hopitaux", Noeud.vide())))
    #noeud3 = n.Noeud("Piscine Olympique", Noeud.vide())
    def test_liste_affichage(self):
        listChain = ListeChainee(Noeud("Erasme", Noeud("CHU Hopitaux", Noeud.vide())))
        self.assertEqual("Erasme CHU Hopitaux", listChain.affichage())
        #si liste vide
        self.assertEqual("", Noeud.vide().affichage())

    def test_liste_longeur(self):
        listChain = ListeChainee(Noeud("Erasme", Noeud("CHU Hopitaux", Noeud.vide())))
        self.assertEqual(2, listChain.get_longueur())

    def test_liste_ajout(self):
        listChain = ListeChainee(Noeud("Erasme", Noeud("CHU Hopitaux", Noeud.vide())))
        listChain.set_tete(listChain.ajoute_fin("Piscine Olympique"))
        self.assertEqual("Erasme CHU Hopitaux Piscine Olympique", listChain.affichage())

    def test_liste_toList(self):
        listChain = ListeChainee(Noeud("Erasme", Noeud("CHU Hopitaux", Noeud.vide())))
        self.assertEqual(["Erasme", "CHU Hopitaux"], listChain.parcourir())

if __name__ == '__main__':
    unittest.main()