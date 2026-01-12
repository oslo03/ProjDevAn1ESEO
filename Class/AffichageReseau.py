import matplotlib.pyplot as plt
import math
from matplotlib.colors import LinearSegmentedColormap


class AffichageReseau:
    """
    Classe responsable de l'affichage graphique du réseau urbain :
    - heatmaps des matrices (temps et distances)
    - affichage du réseau complet
    - affichage du plus court chemin
    - comparaison de trajets
    """

    def __init__(self, reseau):
        """
        Initialise l'affichage à partir d'un réseau urbain.
        - reseau : instance de ReseauUrbain
        """
        self.reseau = reseau
        self.stations = [s.nom for s in reseau.stations]
        self.index = reseau.index_par_nom

    # HEATMAP MATRICE
    # Bleu (faible) -> Rouge (élevé)
    # Les valeurs -1 (absence de liaison) sont affichées en blanc
    def heatmap(self, matrice, titre):
        """
        Affiche une heatmap d'une matrice d'adjacence (temps ou distance).
        """
        n = len(matrice)

        # Conversion de la matrice en valeurs numériques exploitables
        # Les -1 sont remplacés par NaN pour être affichés en blanc
        data = []
        for i in range(n):
            ligne = []
            for j in range(n):
                if matrice[i][j] == -1:
                    ligne.append(float("nan"))
                else:
                    ligne.append(float(matrice[i][j]))
            data.append(ligne)

        # Définition du dégradé bleu → rouge
        cmap = LinearSegmentedColormap.from_list(
            "blue_red",
            ["blue", "red"]
        )
        cmap.set_bad(color="white")

        plt.figure(figsize=(9, 9))
        ax = plt.gca()

        # Affichage de la matrice
        ax.imshow(
            data,
            cmap=cmap,
            origin="upper",
            extent=[0, n, n, 0]
        )

        # Barre de couleur
        plt.colorbar(ax.images[0])

        # Définition de la grille : une case par cellule
        ax.set_xticks(range(n + 1))
        ax.set_yticks(range(n + 1))

        # Placement des labels au centre des cellules
        ax.set_xticks([i + 0.5 for i in range(n)], minor=True)
        ax.set_yticks([i + 0.5 for i in range(n)], minor=True)

        ax.set_xticklabels(self.stations, minor=True, rotation=90)
        ax.set_yticklabels(self.stations, minor=True)

        # Affichage de la grille principale
        ax.grid(which="major", color="black", linewidth=0.6)

        # Masquage des ticks principaux
        ax.tick_params(
            which="major",
            bottom=False,
            left=False,
            labelbottom=False,
            labelleft=False
        )

        plt.title(titre)
        plt.tight_layout()
        plt.show()

    def heatmap_temps(self):
        """
        Heatmap de la matrice des temps (en minutes).
        """
        self.heatmap(self.reseau.matrice_temps, "Heatmap des temps")

    def heatmap_distances(self):
        """
        Heatmap de la matrice des distances (en kilomètres).
        """
        self.heatmap(self.reseau.matrice_distances, "Heatmap des distances")

    # AFFICHAGE DU RÉSEAU COMPLET
    def afficher_reseau_complet(self):
        """
        Affiche le réseau urbain complet sous forme de graphe.
        """
        n = len(self.stations)

        # Placement circulaire des stations
        angles = [2 * math.pi * i / n for i in range(n)]
        pos = {
            self.stations[i]: (
                math.cos(angles[i]),
                math.sin(angles[i])
            )
            for i in range(n)
        }

        plt.figure(figsize=(10, 10))

        # Tracé des arêtes du réseau
        for i in range(n):
            for j in range(i + 1, n):
                if self.reseau.matrice_temps[i][j] != -1:
                    s1 = self.stations[i]
                    s2 = self.stations[j]
                    x1, y1 = pos[s1]
                    x2, y2 = pos[s2]
                    plt.plot(
                        [x1, x2],
                        [y1, y2],
                        color="lightgray",
                        linewidth=2,
                        zorder=1
                    )

        # Tracé des sommets et de leurs labels
        for station, (x, y) in pos.items():
            plt.scatter(x, y, color="black", s=40, zorder=2)
            plt.text(
                x * 1.08,
                y * 1.08,
                station,
                fontsize=10,
                ha="center",
                va="center"
            )

        plt.title("Réseau urbain – vue complète")
        plt.axis("off")
        plt.tight_layout()
        plt.show()

    # DIJKSTRA
    def dijkstra(self, depart, arrivee, matrice):
        """
        Algorithme de Dijkstra permettant de calculer le plus court chemin
        entre deux stations à partir d'une matrice de poids.
        """
        n = len(self.stations)
        depart_i = self.index[depart]
        arrivee_i = self.index[arrivee]

        # Initialisation des structures
        dist = [math.inf] * n
        precedent = [None] * n
        visites = [False] * n

        dist[depart_i] = 0

        # Boucle principale de Dijkstra
        for _ in range(n):
            u = None
            min_dist = math.inf

            # Sélection du sommet non visité le plus proche
            for i in range(n):
                if not visites[i] and dist[i] < min_dist:
                    min_dist = dist[i]
                    u = i

            if u is None:
                break

            visites[u] = True

            # Relaxation des arêtes sortantes
            for v in range(n):
                poids = matrice[u][v]
                if poids != -1 and not visites[v]:
                    if dist[u] + poids < dist[v]:
                        dist[v] = dist[u] + poids
                        precedent[v] = u

        # Si l'arrivée est inatteignable
        if dist[arrivee_i] == math.inf:
            return None, math.inf

        # Reconstruction du chemin
        chemin = []
        cur = arrivee_i
        while cur is not None:
            chemin.insert(0, self.stations[cur])
            cur = precedent[cur]

        return chemin, dist[arrivee_i]

    # AFFICHAGE DU PLUS COURT CHEMIN
    def afficher_plus_court_chemin(self, depart, arrivee, mode="temps"):
        """
        Affiche graphiquement le plus court chemin entre deux stations,
        selon le critère temps ou distance.
        """
        matrice = (
            self.reseau.matrice_temps
            if mode == "temps"
            else self.reseau.matrice_distances
        )

        chemin, cout = self.dijkstra(depart, arrivee, matrice)

        if chemin is None:
            print("Aucun chemin possible.")
            return

        # Mise en forme du coût avec unité
        if mode == "temps":
            cout_affiche = f"{round(cout)} min"
        else:
            cout_affiche = f"{round(cout)} km"

        self._affichage_graphe(
            chemins=[(chemin, "red")],
            titre=f"Plus court chemin ({mode}) – coût ≈ {cout_affiche}"
        )

    # COMPARAISON DE DEUX TRAJETS
    def afficher_deux_trajets(self, trajet1, trajet2):
        """
        Affiche deux trajets différents sur le même graphe
        afin de permettre leur comparaison visuelle.
        """
        self._affichage_graphe(
            chemins=[
                (trajet1, "red"),
                (trajet2, "blue")
            ],
            titre="Comparaison de deux trajets"
        )

    # AFFICHAGE GRAPHIQUE DES CHEMINS
    def _affichage_graphe(self, chemins, titre):
        """
        Affiche un graphe contenant uniquement les chemins fournis.
        """
        n = len(self.stations)

        angles = [2 * math.pi * i / n for i in range(n)]
        pos = {
            self.stations[i]: (
                math.cos(angles[i]),
                math.sin(angles[i])
            )
            for i in range(n)
        }

        plt.figure(figsize=(10, 10))

        # Affichage des sommets
        for station, (x, y) in pos.items():
            plt.scatter(x, y, color="black", zorder=2)
            plt.text(
                x * 1.08,
                y * 1.08,
                station,
                fontsize=10,
                ha="center",
                va="center"
            )

        # Affichage des chemins
        for chemin, couleur in chemins:
            for i in range(len(chemin) - 1):
                x1, y1 = pos[chemin[i]]
                x2, y2 = pos[chemin[i + 1]]
                plt.plot(
                    [x1, x2],
                    [y1, y2],
                    color=couleur,
                    linewidth=4,
                    zorder=3
                )

        plt.title(titre)
        plt.axis("off")
        plt.tight_layout()
        plt.show()
