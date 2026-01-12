from Class.ReseauUrbain import ReseauUrbain
from Class.AffichageReseau import AffichageReseau

# AFFICHAGE DU MENU PRINCIPAL
def afficher_menu():
    """
    Affiche le menu interactif et récupère le choix de l'utilisateur.
    """
    print("\n==================== MENU ====================")
    print("1 - Afficher la heatmap des temps")
    print("2 - Afficher la heatmap des distances")
    print("3 - Afficher le réseau complet")
    print("4 - Plus court chemin (temps)")
    print("5 - Plus court chemin (distance)")
    print("6 - Comparer deux trajets")
    print("0 - Quitter")
    return input("Choix : ").strip()


# VÉRIFICATION D'UNE STATION
def station_valide(nom, reseau):
    """
    Vérifie si le nom d'une station existe dans le réseau.
    """
    return nom in reseau.index_par_nom


# DEMANDE D'UNE STATION À L'UTILISATEUR
def demander_station(message, reseau):
    """
    Demande à l'utilisateur de saisir une station valide.
    Répète la demande tant que la station est inconnue.
    """
    while True:
        nom = input(message).strip()
        if station_valide(nom, reseau):
            return nom
        print("Station inconnue. Veuillez réessayer.")


# DEMANDE D'UN TRAJET (LISTE DE STATIONS)
def demander_trajet(message, reseau):
    """
    Demande à l'utilisateur un trajet sous forme de stations
    séparées par des virgules et vérifie leur validité.
    """
    while True:
        saisie = input(message).strip()
        stations = [s.strip() for s in saisie.split(",") if s.strip()]

        # Un trajet doit contenir au minimum deux stations
        if len(stations) < 2:
            print("Un trajet doit contenir au moins deux stations.")
            continue

        # Vérification des stations inconnues
        inconnues = [s for s in stations if not station_valide(s, reseau)]
        if inconnues:
            print("Stations inconnues :", ", ".join(inconnues))
            continue

        return stations


# PROGRAMME PRINCIPAL
if __name__ == '__main__':

    # CRÉATION ET CHARGEMENT DU RÉSEAU
    reseau = ReseauUrbain("RER B")
    reseau.charger_depuis_csv()

    print(reseau)

    # AFFICHAGE DES MATRICES (MODE DEBUG / CONTRÔLE)
    print("\nMatrice des temps :")
    for ligne in reseau.matrice_temps:
        print(ligne)

    print("\nMatrice des distances :")
    for ligne in reseau.matrice_distances:
        print(ligne)

    # LISTE DES STATIONS DISPONIBLES
    print("\nStations du réseau :")
    for nom in reseau.index_par_nom.keys():
        print("-", nom)

    # TEST DE LA MÉTHODE voisins
    station_test = "Centre"
    print(f"\nVoisins de {station_test} :")
    try:
        voisins = reseau.voisins(station_test)
        print(voisins)
    except ValueError as e:
        print("Erreur :", e)

    # INITIALISATION DU MODULE D'AFFICHAGE
    affichage = AffichageReseau(reseau)

    # BOUCLE INTERACTIVE PRINCIPALE
    while True:
        choix = afficher_menu()

        # --- Heatmap des temps ---
        if choix == "1":
            affichage.heatmap_temps()

        # --- Heatmap des distances ---
        elif choix == "2":
            affichage.heatmap_distances()

        # --- Affichage global du réseau ---
        elif choix == "3":
            affichage.afficher_reseau_complet()

        # --- Plus court chemin en temps ---
        elif choix == "4":
            depart = demander_station("Station de départ : ", reseau)
            arrivee = demander_station("Station d'arrivée : ", reseau)

            chemin, cout = affichage.dijkstra(
                depart,
                arrivee,
                reseau.matrice_temps
            )

            if chemin is None:
                print("Aucun chemin possible.")
            else:
                print(f"Temps minimal ≈ {round(cout)} minutes")
                affichage.afficher_plus_court_chemin(depart, arrivee, mode="temps")

        # --- Plus court chemin en distance ---
        elif choix == "5":
            depart = demander_station("Station de départ : ", reseau)
            arrivee = demander_station("Station d'arrivée : ", reseau)

            chemin, cout = affichage.dijkstra(
                depart,
                arrivee,
                reseau.matrice_distances
            )

            if chemin is None:
                print("Aucun chemin possible.")
            else:
                print(f"Distance minimale ≈ {round(cout)} km")
                affichage.afficher_plus_court_chemin(depart, arrivee, mode="distance")

        # --- Comparaison de deux trajets ---
        elif choix == "6":
            trajet_1 = demander_trajet(
                "Entrer le premier trajet (stations séparées par des virgules) : ",
                reseau
            )
            trajet_2 = demander_trajet(
                "Entrer le second trajet (stations séparées par des virgules) : ",
                reseau
            )

            affichage.afficher_deux_trajets(trajet_1, trajet_2)

        # --- Quitter le programme ---
        elif choix == "0":
            print("Fin du programme.")
            break

        # --- Choix invalide ---
        else:
            print("Choix invalide. Veuillez sélectionner une option valide.")
