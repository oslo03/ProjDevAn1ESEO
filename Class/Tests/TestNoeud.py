import unittest

from Class.Noeud import Noeud

class TestNoeud(unittest.TestCase):
    #les autres fonctions sont testé dans le programme de test Unitaire de ListeChainee.
    def test_est_vide(self):
        neoud = Noeud.vide()
        self.assertEqual(True, neoud.est_vide())

if __name__ == '__main__':
    unittest.main()