from Class.ListeChainee import ListeChainee
from Class.Noeud import Noeud
import unittest

#Classe de trajet observée, avec la liste des stations parcourus et la meusure de temps et de distance.

class TrajetObserve:
    def __init__(self, idTraj, nomsStations, tpsMesure, distMesure):
        self.idTraj=idTraj
        self.nomsStations = nomsStations
        self.tpsMesure = tpsMesure
        self.distMesure = distMesure

    def Conv_Liste_Chainee(self):
        #Création d'une liste chainée avec les données de l'objet.
        result=LstChaine.ListeChainee(n.Noeud.vide())
        for i in self.nomsStations:
            result=result.ajoute_fin(i)
        return result


class TestTrajetObserve(unittest.TestCase):
    def test_converstion(self):
        trajOb1=TrajetObserve(1, ["Erasme", "Piscine Olympique"], 12, 2)
        listChain=trajOb1.Conv_Liste_Chainee()
        self.assertEqual("Erasme Piscine Olympique", listChain.affichage())

if __name__ == '__main__':
    unittest.main()