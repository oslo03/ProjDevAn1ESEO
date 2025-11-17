import csv
import glob

def execCSV():
    files = glob.glob('./csv_files/reseau_xl/*.csv')

    if not files:
        print("Aucun fichier CSV trouvé !")
        return

    for filename in files:
        print(f"Lecture du fichier : {filename}")
        with open(filename, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in spamreader:
                print(', '.join(row))
