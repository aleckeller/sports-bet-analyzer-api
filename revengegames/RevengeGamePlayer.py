class RevengeGamePlayer():
    def __init__(self, player, current_team):
        self.player = player
        self.id = player.player_id 
        self.name = player.name
        self.current_team = current_team
    
    def to_string(self):
        the_string = f"""
        Name: {self.name}
        Current Team: {self.current_team.name}
        """
        return the_string
    
    def to_object(self):
        player = {
            "name": self.name,
            "current_team": self.current_team.name
        }
        return player