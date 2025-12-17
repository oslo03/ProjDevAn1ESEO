from Class.ReseauUrbain import ReseauUrbain

if __name__ == '__main__':

    # Création du réseau
    reseau = ReseauUrbain("RER B")

    # Chargement des stations et des routes depuis les CSV
    reseau.charger_depuis_csv()

    # Affichage du réseau
    print(reseau)

    print("\nMatrice des temps :")
    for ligne in reseau.matrice_temps:
        print(ligne)

    print("\nMatrice des distances :")
    for ligne in reseau.matrice_distances:
        print(ligne)

    # Test de la méthode voisins
    print("\nVoisins de Clichy :")
    print(reseau.voisins("Clichy"))
