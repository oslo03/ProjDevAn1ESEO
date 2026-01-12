import unittest

from Class.ListeChainee import ListeChainee
from Class.Noeud import Noeud

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