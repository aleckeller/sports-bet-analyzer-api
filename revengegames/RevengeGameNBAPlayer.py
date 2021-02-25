from revengegames.RevengeGamePlayer import RevengeGamePlayer

class RevengeGameNBAPlayer(RevengeGamePlayer):
    def __init__(self, player, current_team, previous_team_years):
        super().__init__(player, current_team, previous_team_years)
        
    
    def to_string(self):
        string = super().to_string()
        string = string + f"""
        Usage Percentage: {self.player.usage_percentage}
        Minutes Played: {self.player.minutes_played}
        """
        return string
    
    def to_object(self):
        data = super().to_object()
        data["usage_percentage"] = self.player.usage_percentage
        data["minutes_played"] = self.player.minutes_played
        return data