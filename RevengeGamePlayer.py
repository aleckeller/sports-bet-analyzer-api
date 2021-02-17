import json

class RevengeGamePlayer:
    def __init__(self, id: str, name: str, current_team: str, details):
        self.id = id
        self.name = name
        self.current_team = current_team
        self.details = details
    
    def to_string(self):
        the_string = f"""
        Name: {self.name}
        Current Team: {self.current_team}
        Usage Percentage: {self.details.usage_percentage}
        """
        return the_string
    
    def to_object(self):
        player = {
            "name": self.name,
            "current_team": self.current_team
        }
        return player