import unittest
import TrajetObserve.py

class TestTrajetObserve(unittest.TestCase):
    def test_converstion(self):
        trajOb1=TrajetObserve(1, ["Erasme", "Piscine Olympique"], 12, 2)
        listChain=trajOb1.Conv_Liste_Chainee()
        self.assertEqual("Erasme Piscine Olympique", listChain.affichage())
