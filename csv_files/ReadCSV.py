import csv

BASE_PATH = "./csv_files/reseau_xl/"

def load_csv_stations():
    stations = []
    with open(BASE_PATH + "stations_xl.csv", newline='', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)  # saut de l'en-tête
        for row in reader:
            if not row:
                continue
            station_id = int(row[0])
            nom_station = row[1].strip()   # correction importante
            stations.append((station_id, nom_station))
    return stations


def load_csv_roads():
    routes = []
    with open(BASE_PATH + "routes_xl.csv", newline='', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)
        for row in reader:
            if not row:
                continue
            depart = row[0].strip()        # correction importante
            arrivee = row[1].strip()       # correction importante
            distance = float(row[2])
            temps = float(row[3])
            routes.append((depart, arrivee, distance, temps))
    return routes


def load_csv_trajets():
    trajets = []
    with open(BASE_PATH + "trajets_xl.csv", newline='', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)
        for row in reader:
            if not row:
                continue
            id_trajet = row[0].strip()
            stations = [s.strip() for s in row[1].split(";")]  # nettoyage
            temps_mesure = float(row[2])
            distance_mesuree = float(row[3])
            trajets.append((id_trajet, stations, temps_mesure, distance_mesuree))
    return trajets


def printCSV(filename):
    with open(BASE_PATH + filename, newline='', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            print(row)
