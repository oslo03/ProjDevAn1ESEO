from Class.ReseauUrbain import ReseauUrbain

if __name__ == '__main__':

    # Création du réseau
    reseau = ReseauUrbain("RER B")

    # Chargement des stations et des routes depuis les CSV
    reseau.charger_depuis_csv()

    # Affichage du réseau
    print(reseau)

    # Affichage des matrices
    print("\nMatrice des temps :")
    for ligne in reseau.matrice_temps:
        print(ligne)

    print("\nMatrice des distances :")
    for ligne in reseau.matrice_distances:
        print(ligne)

    # Affichage des stations connues (IMPORTANT pour debug)
    print("\nStations du réseau :")
    for nom in reseau.index_par_nom.keys():
        print("-", nom)

    # Test de la méthode voisins (protégé)
    station_test = "Clichy"

    print(f"\nVoisins de {station_test} :")
    try:
        voisins = reseau.voisins(station_test)
        print(voisins)
    except ValueError as e:
        print("Erreur :", e)
