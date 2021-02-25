from datetime import datetime
from urllib.error import HTTPError
import dateutil.parser

from revengegames.RevengeGame import RevengeGame
from revengegames.RevengeGamePlayer import RevengeGamePlayer
from revengegames.RevengeGameTeam import RevengeGameTeam
import revengegames.sports_objects as sports_objects
import revengegames.CONSTANTS as CONSTANTS

class RevengeGameGenerator:
    def __init__(self, sport: str, years_back: int, date_of_games: datetime):
        self.sport = sport
        self.years_back = years_back
        self.date_of_games = date_of_games
    
    def get_revenge_games(self):
        revenge_games = []
        games = self.get_games_today()
        for game in games:
            revenge_game = self.get_revenge_game(game, is_revenge_game=False, switched=False)
            if revenge_game:
                revenge_games.append(game)
        return revenge_games
    
    def get_revenge_game(self, game, is_revenge_game=False, switched=False):
        if not switched:
            team_one = game.home_team
            team_two = game.away_team
        else:
            team_one = game.away_team
            team_two = game.home_team
        team_one_roster = self.get_team_roster(team_one.abbreviation, self.date_of_games.year, True)
        team_two_roster = self.get_roster_within_years(team_two.abbreviation, self.years_back)
        revenge_game = None
        for player in team_one_roster.players.items():
            player_id = player[0]
            if team_two_roster.get(player_id):
                is_revenge_game = True
                player_previous_team_years = team_two_roster[player_id].get("years")
                revenge_game_player = sports_objects.get_sport_object(self.sport, CONSTANTS.REVENGE_GAME_PLAYER)
                revenge_game_player = revenge_game_player(self.get_player(player_id), team_one, player_previous_team_years)
                game.revenge_game_players.append(revenge_game_player)

        if not switched:
            revenge_game = self.get_revenge_game(game, is_revenge_game, True)
        elif is_revenge_game:
            revenge_game = game
        return revenge_game
    
    def get_games_today(self):
        teams = self.get_teams(year=self.date_of_games.year)
        teams_playing_today = []
        games_today = []
        for team in teams:
            if (team.abbreviation not in teams_playing_today):
                game = self.get_team_todays_game(team.abbreviation)
                if (game):
                    sports_reference_team = self.get_teams(team_abbreviation=game.opponent_abbr)
                    if sports_reference_team:
                        if game.location == CONSTANTS.HOME:
                            home_team = RevengeGameTeam(team)
                            away_team = RevengeGameTeam(sports_reference_team)
                        else:
                            home_team = RevengeGameTeam(sports_reference_team)
                            away_team = RevengeGameTeam(team)
                        teams_playing_today.append(home_team.abbreviation)
                        teams_playing_today.append(away_team.abbreviation)
                        revengeGame = RevengeGame(home_team, away_team, [])
                        games_today.append(revengeGame)
        return games_today
    
    def get_team_todays_game(self, team_abbreviation):
        now_formatted = self.date_of_games.strftime("%m-%d-%Y")
        todays_game = None
        game_found = False
        schedule = self.get_team_schedule(team_abbreviation)
        if (schedule):
            for game in schedule:
                if (not game_found):
                    date_time_obj = dateutil.parser.parse(game.date).strftime("%m-%d-%Y")
                    if (date_time_obj == now_formatted):
                        game_found = True
                        todays_game = game
        return todays_game

    def get_roster_within_years(self, team_abbreviation, years_back):
        timeline_roster = {}
        for num_of_years in range(0, years_back + 1):
            year_to_check = self.date_of_games.year - num_of_years
            roster = self.get_team_roster(team_abbreviation, year_to_check, True)
            for player in roster.players.items():
                player_id = player[0]
                player_name = player[1]
                if player_id in timeline_roster.keys():
                    # Get player from timeline_roster and add year to array
                    years = timeline_roster[player_id]["years"]
                    years.append(year_to_check)
                    timeline_roster[player_id]["years"] = years
                else:
                    # Add player to timeline_roster and init year array
                    timeline_roster[player_id] = {
                        "name": player_name,
                        "years": [year_to_check]
                    }
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

    def get_teams(self, team_abbreviation=None, year=None):
        teams = sports_objects.get_sport_object(self.sport, CONSTANTS.TEAMS)
        if teams:
            try:
                if team_abbreviation:
                    team = teams()
                    return team(team_abbreviation)
                elif year:
                    return teams(year = year)
                else:
                    print("Need to provide year or team abbreviation!")
                    return None
            except HTTPError:
                if team_abbreviation:
                    print(team_abbreviation + " does not have a team!")
                elif year:
                    print(year + " does not have any teams!")
                else:
                    print("Need to provide year or team abbreviation!")
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
    
    def get_revenge_game_player(self):
        revenge_game_player = sports_objects.get_sport_object(self.sport, CONSTANTS.REVENGE_GAME_PLAYER)
        return revenge_game_player