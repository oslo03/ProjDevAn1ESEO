from Class.Station import Station
from csv_files.ReadCSV import load_csv_stations, load_csv_roads

class ReseauUrbain:

    def __init__(self, nom):
        self.nom = nom
        self.stations = []
        self.index_par_nom = {}
        self.matrice_distances = []
        self.matrice_temps = []

    def ajouter_station(self, nom_station):
        if nom_station in self.index_par_nom:
            return

        index = len(self.stations)
        station = Station(index, nom_station)

        self.stations.append(station)
        self.index_par_nom[nom_station] = index

        for ligne in self.matrice_distances:
            ligne.append(-1)
        for ligne in self.matrice_temps:
            ligne.append(-1)

        self.matrice_distances.append([-1] * (index + 1))
        self.matrice_temps.append([-1] * (index + 1))

    def ajouter_route(self, station_depart, station_arrivee, distance, temps):
        if station_depart not in self.index_par_nom or station_arrivee not in self.index_par_nom:
            raise ValueError(f"Station inconnue : {station_depart} ou {station_arrivee}")

        i = self.index_par_nom[station_depart]
        j = self.index_par_nom[station_arrivee]

        # réseau réciproque (non orienté)
        self.matrice_distances[i][j] = distance
        self.matrice_distances[j][i] = distance

        self.matrice_temps[i][j] = temps
        self.matrice_temps[j][i] = temps

    def voisins(self, nom_station):
        if nom_station not in self.index_par_nom:
            raise ValueError("Station inconnue")

        index = self.index_par_nom[nom_station]
        return [
            self.stations[j].nom
            for j in range(len(self.stations))
            if self.matrice_temps[index][j] != -1
        ]

    def charger_depuis_csv(self):
        # --- Chargement des stations ---
        stations = load_csv_stations()

        id_to_nom = {}
        for station_id, nom_station in stations:
            id_to_nom[str(station_id)] = nom_station
            self.ajouter_station(nom_station)

        # --- Chargement des routes ---
        routes = load_csv_roads()
        for depart_id, arrivee_id, distance, temps in routes:
            depart_nom = id_to_nom[depart_id]
            arrivee_nom = id_to_nom[arrivee_id]
            self.ajouter_route(depart_nom, arrivee_nom, distance, temps)

    def affichage_matrices(self):
        print("Matrice des distances :")
        for ligne in self.matrice_distances:
            print(ligne)

        print("\nMatrice des temps :")
        for ligne in self.matrice_temps:
            print(ligne)

    def __str__(self):
        return f"Réseau {self.nom} avec {len(self.stations)} stations"
