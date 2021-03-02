import utils

class RevengeGameTeam():

    def __init__(self, team, metrics):
        self.name = team.name
        self.abbreviation = team.abbreviation
        self.team = team
        self.metrics = metrics
        self.data_dictionary = self.to_dictionary()
    
    def to_dictionary(self):
        team_dict = {
            "name": self.name,
            "abbreviation": self.abbreviation
        }
        metrics_dict = utils.create_metrics_object(self.metrics, self.team)
        team_dict.update(metrics_dict)
        return team_dict