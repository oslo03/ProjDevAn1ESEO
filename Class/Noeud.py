class Noeud:
    """
    Classe représentant un noeud d'une liste simplement chaînée.
    Chaque noeud contient une valeur et un pointeur vers le noeud suivant.
    """

    def __init__(self, valeur):
        self.valeur = valeur
        self.suivant = None

"test de la classe Noeud"
if __name__ == "__main__":
    print("=== Test de la classe Noeud ===")

    # Création de deux noeuds
    n1 = Noeud("Station A")
    n2 = Noeud("Station B")

    # On relie n1 -> n2
    n1.suivant = n2

    # Vérification des valeurs
    print("n1.valeur =", n1.valeur)
    print("n1.suivant.valeur =", n1.suivant.valeur)
    print("n2.valeur =", n2.valeur)
    print("n2.suivant =", n2.suivant)  # doit afficher None

    print("=== Fin du test ===")
