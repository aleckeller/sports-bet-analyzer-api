class RevengeGameTeam():

    def __init__(self, team):
        self.name = team.name
        self.abbreviation = team.abbreviation
        self.team = team

    def to_string(self):
        the_string = f"""
        Name: {self.name}
        Abbreviation: {self.abbreviation}
        """
        return the_string
    
    def to_object(self):
        team = {
            "name": self.name,
            "abbreviation": self.abbreviation
        }
        return team