from Class.Station import Station
from csv_files.ReadCSV import load_csv_stations, load_csv_roads


class ReseauUrbain:
    """
    Classe représentant un réseau urbain modélisé sous forme de graphe.
    Les stations sont les sommets et les routes sont représentées
    par des matrices d’adjacence (temps et distances).
    """

    def __init__(self, nom):
        """
        Initialise un réseau urbain vide.

        :param nom: nom du réseau (ex : RER B)
        """
        self.nom = nom
        self.stations = []              # Liste des objets Station
        self.index_par_nom = {}         # Dictionnaire nom -> index
        self.matrice_distances = []     # Matrice d’adjacence des distances
        self.matrice_temps = []         # Matrice d’adjacence des temps

    # AJOUT D'UNE STATION
    def ajouter_station(self, nom_station):
        """
        Ajoute une station au réseau si elle n'existe pas déjà.
        Met à jour les matrices d’adjacence en conséquence.
        """
        # Évite les doublons
        if nom_station in self.index_par_nom:
            return

        # Index de la nouvelle station
        index = len(self.stations)

        # Création de l’objet Station
        station = Station(index, nom_station)

        # Ajout à la liste des stations
        self.stations.append(station)
        self.index_par_nom[nom_station] = index

        # Extension des lignes existantes des matrices
        for ligne in self.matrice_distances:
            ligne.append(-1)
        for ligne in self.matrice_temps:
            ligne.append(-1)

        # Ajout d’une nouvelle ligne pour la station
        self.matrice_distances.append([-1] * (index + 1))
        self.matrice_temps.append([-1] * (index + 1))

    # AJOUT D'UNE ROUTE ENTRE DEUX STATIONS
    def ajouter_route(self, station_depart, station_arrivee, distance, temps):
        """
        Ajoute une route entre deux stations existantes.
        Le réseau est considéré comme non orienté (réciproque).
        """
        # Vérification de l’existence des stations
        if station_depart not in self.index_par_nom or station_arrivee not in self.index_par_nom:
            raise ValueError(f"Station inconnue : {station_depart} ou {station_arrivee}")

        # Récupération des indices des stations
        i = self.index_par_nom[station_depart]
        j = self.index_par_nom[station_arrivee]

        # Mise à jour des matrices (liaison bidirectionnelle)
        self.matrice_distances[i][j] = distance
        self.matrice_distances[j][i] = distance

        self.matrice_temps[i][j] = temps
        self.matrice_temps[j][i] = temps

    # RÉCUPÉRATION DES VOISINS D'UNE STATION
    def voisins(self, nom_station):
        """
        Retourne la liste des stations directement accessibles
        depuis une station donnée.
        """
        if nom_station not in self.index_par_nom:
            raise ValueError("Station inconnue")

        index = self.index_par_nom[nom_station]

        return [
            self.stations[j].nom
            for j in range(len(self.stations))
            if self.matrice_temps[index][j] != -1
        ]

    # CHARGEMENT DU RÉSEAU DEPUIS DES FICHIERS CSV
    def charger_depuis_csv(self):
        """
        Construit le réseau à partir de fichiers CSV :
        - un fichier pour les stations
        - un fichier pour les routes
        """
        # Chargement des stations
        stations = load_csv_stations()

        # Dictionnaire temporaire id -> nom
        id_to_nom = {}
        for station_id, nom_station in stations:
            id_to_nom[str(station_id)] = nom_station
            self.ajouter_station(nom_station)

        # Chargement des routes
        routes = load_csv_roads()
        for depart_id, arrivee_id, distance, temps in routes:
            depart_nom = id_to_nom[depart_id]
            arrivee_nom = id_to_nom[arrivee_id]
            self.ajouter_route(depart_nom, arrivee_nom, distance, temps)

    # AFFICHAGE DES MATRICES
    def affichage_matrices(self):
        """
        Affiche les matrices de distances et de temps dans la console.
        Utile pour le débogage.
        """
        print("Matrice des distances :")
        for ligne in self.matrice_distances:
            print(ligne)

        print("\nMatrice des temps :")
        for ligne in self.matrice_temps:
            print(ligne)

    # REPRÉSENTATION TEXTE DU RÉSEAU
    def __str__(self):
        """
        Représentation textuelle du réseau.
        """
        return f"Réseau {self.nom} avec {len(self.stations)} stations"
