from Class.ReseauUrbain import ReseauUrbain
from csv_files.ReadCSV import printCSV


if __name__ == '__main__':
    #Mon reseau
    reseau = ReseauUrbain("RER B")

    #Les stations de mon reseau

    reseau.addStation("Clichy")
    reseau.addStation("BarbesRochechoire")
    reseau.addStation("Sevran")

    #La route de mon reseau, l'intervalle entre de station
    reseau.addRoad("BarbesRochechoire", "Clichy", 10, 2000)
    reseau.addRoad("BarbesRochechoire", "Sevran", 20, 4000)
    reseau.addRoad("Clichy", "BarbesRochechoire", 30, 7000)
    reseau.addRoad("Clichy", "Sevran", 40, 5000)
    reseau.addRoad("Sevran", "BarbesRochechoire", 50, 1000)
    reseau.addRoad("Sevran", "Clichy", 60, 3000)

    print("Matrice durées :")
    print(reseau.timeMat)

    print("Matrice distances :")
    print(reseau.distMat)

    ##printCSV()
