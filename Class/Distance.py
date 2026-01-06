class Distance:
    def __init__(self, distance_theorique, temps_theorique, segments_inexistants):
        self.distance_theorique = distance_theorique
        self.temps_theorique = temps_theorique
        self.segments_inexistants = segments_inexistants

    def __str__(self):
        return (
            f"Distance théorique: {self.distance_theorique}, "
            f"Temps théorique: {self.temps_theorique}, "
            f"Segments inexistants: {self.segments_inexistants}"
        )
