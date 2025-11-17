import csv
import glob

def load_csv_files():
    files = glob.glob('./csv_files/reseau_xl/*.csv')
    if not files:
        print("Aucun fichier CSV trouvé !")
    return files
    data = []
    for filename in files:
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            table = [row for row in reader]
            data.append(table)
    return data

def printCSV():
    files = load_csv_files()

    for filename in files:
        print(f"Lecture du fichier : {filename}")
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in reader:
                print(', '.join(row))
