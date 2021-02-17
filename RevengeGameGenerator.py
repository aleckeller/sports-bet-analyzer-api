from datetime import datetime
from urllib.error import HTTPError
import dateutil.parser

from RevengeGame import RevengeGame
from RevengeGamePlayer import RevengeGamePlayer
import sports_objects
import CONSTANTS

class RevengeGameGenerator:
    def __init__(self, sport: str, years_back: int, date_of_games: datetime):
        self.sport = sport
        self.years_back = years_back
        self.date_of_games = date_of_games
    
    def get_revenge_games(self):
        revenge_games = []
        games = self.get_games_today()
        for game in games:
            revenge_game = self.get_revenge_game(game[0], game[1], is_revenge_game=False, revenge_game_players=[], switched=False)
            if revenge_game:
                revenge_games.append(revenge_game)
        return revenge_games
    
    def get_revenge_game(self, team_one_abbreviation, team_two_abbreviation, is_revenge_game=False, revenge_game_players=[], switched=False):
        roster = self.get_team_roster(team_one_abbreviation, self.date_of_games.year, True)
        other_roster = self.get_roster_within_years(team_two_abbreviation, self.years_back)
        revenge_game = None
        for player in roster.players.items():
            if player in other_roster:
                is_revenge_game = True
                revenge_game_player = RevengeGamePlayer(player[0], player[1], team_one_abbreviation, self.get_player(player[0]))
                revenge_game_players.append(revenge_game_player)

        if not switched:
            revenge_game = self.get_revenge_game(team_two_abbreviation, team_one_abbreviation, is_revenge_game, revenge_game_players, True)
        elif is_revenge_game:
            revenge_game = RevengeGame(team_one_abbreviation, team_two_abbreviation, revenge_game_players)
        return revenge_game
    
    def get_games_today(self):
        teams = self.get_teams_in_year(self.date_of_games.year)
        teams_playing_today = []
        games_today = []
        for team in teams:
            if (team.abbreviation not in teams_playing_today):
                game = self.get_team_todays_game(team.abbreviation)
                if (game):
                    teams_playing_today.append(team.abbreviation)
                    teams_playing_today.append(game.opponent_abbr)
                    games_today.append((team.abbreviation, game.opponent_abbr))
        return games_today
    
    def get_team_todays_game(self, team_abbreviation):
        now_formatted = self.date_of_games.strftime("%Y-%m-%d")
        todays_game = None
        game_found = False
        schedule = self.get_team_schedule(team_abbreviation)
        if (schedule):
            for game in schedule:
                if (not game_found):
                    date_time_obj = dateutil.parser.parse(game.date).strftime("%Y-%m-%d")
                    if (date_time_obj == now_formatted):
                        game_found = True
                        todays_game = game
        return todays_game

    def get_roster_within_years(self, team_abbreviation, years_back):
        timeline_roster = []
        for num_of_years in range(0, years_back + 1):
            year_to_check = self.date_of_games.year - num_of_years
            roster = self.get_team_roster(team_abbreviation, year_to_check, True)
            for player in roster.players.items():
                if player not in timeline_roster:
                    timeline_roster.append(player)
        return timeline_roster

    def has_player_been_on_team_in_year(self, player_to_be_searched_name, roster, year):
        player_has_been_on_team = False
        for player in roster.players:
            if player.name == player_to_be_searched_name:
                player_has_been_on_team = True
                break
        return player_has_been_on_team

    def get_team_schedule(self, team_abbreviation):
        schedule = sports_objects.get_sport_object(self.sport, CONSTANTS.SCHEDULE)
        if schedule:
            try:
                return schedule(team_abbreviation)
            except HTTPError:
                print(team_abbreviation + " does not have a schedule!")
                return None
        else:
            return None

    def get_teams_in_year(self, year):
        teams = sports_objects.get_sport_object(self.sport, CONSTANTS.TEAMS)
        if teams:
            try:
                return teams(year = year)
            except HTTPError:
                print(year + " does not have any teams!")
                return None
        else:
            return None

    def get_team_roster(self, team_abbreviation, year, slim=False):
        roster = sports_objects.get_sport_object(self.sport, CONSTANTS.ROSTER)
        if roster:
            try:
                return roster(team_abbreviation, year, slim)
            except HTTPError:
                print(team_abbreviation + " does not a roster!")
                return None
        else:
            return None

    def get_player(self, player_id):
        player = sports_objects.get_sport_object(self.sport, CONSTANTS.PLAYER)
        if player:
            try:
                return player(player_id)
            except HTTPError:
                print(player_id + " does not exist!")
                return None
        else:
            return None