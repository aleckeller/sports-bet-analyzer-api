from revengegames.RevengeGamePlayer import RevengeGamePlayer

class RevengeGameNHLPlayer(RevengeGamePlayer):
    def __init__(self, player, current_team, previous_team_years):
        super().__init__(player, current_team, previous_team_years)
        
    
    def to_string(self):
        string = super().to_string()
        string = string + f"""
        Corsi for Percentage: {self.player.corsi_for_percentage}
        Goals: {self.player.goals}
        """
        return string
    
    def to_object(self):
        data = super().to_object()
        data["corsi_for_percentage"] = self.player.corsi_for_percentage
        data["goals"] = self.player.goals
        return data