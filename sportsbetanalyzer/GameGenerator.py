from datetime import datetime
from urllib.error import HTTPError
import dateutil.parser

from sportsbetanalyzer.Game import Game
from sportsbetanalyzer.Player import Player
from sportsbetanalyzer.Team import Team
import sportsbetanalyzer.sports_objects as sports_objects
import sportsbetanalyzer.CONSTANTS as CONSTANTS

class GameGenerator:
    def __init__(self, league: str, date_of_games: datetime, json_logic: object):
        self.league = league
        self.date_of_games = date_of_games
        self.json_logic = json_logic
    
    def get_games(self, slim_roster=False):
        teams = self.get_teams(year=self.date_of_games.year)
        teams_playing_today = []
        games_today = []
        for team in teams:
            if (team.abbreviation not in teams_playing_today):
                game = self.get_game_for_team(team.abbreviation)
                if (game):
                    print("Working on " + team.abbreviation + " vs. " + game.opponent_abbr)
                    sports_reference_team = self.get_teams(team_abbreviation=game.opponent_abbr)
                    if sports_reference_team:
                        player_metrics, player_rules = self.get_rules_and_metrics(CONSTANTS.PLAYER_KEY)
                        if slim_roster:
                            team_roster = self.get_sports_reference_roster(team.abbreviation, self.date_of_games.year, True)
                            sports_reference_roster = self.get_sports_reference_roster(sports_reference_team.abbreviation, self.date_of_games.year, True)
                        else:
                            team_roster = self.get_team_roster(team.abbreviation, self.date_of_games.year, player_metrics, player_rules)
                            sports_reference_roster = self.get_team_roster(sports_reference_team.abbreviation, self.date_of_games.year, player_metrics, player_rules)
                        team_metrics, team_rules = self.get_rules_and_metrics(CONSTANTS.TEAM_KEY)
                        if game.location == CONSTANTS.HOME:
                            home_team = Team(team, team_metrics, team_roster, team_rules)
                            away_team = Team(sports_reference_team, team_metrics, sports_reference_roster, team_rules)
                        else:
                            home_team = Team(sports_reference_team, team_metrics, sports_reference_roster, team_rules)
                            away_team = Team(team, team_metrics, team_roster, team_rules)
                        teams_playing_today.append(home_team.abbreviation)
                        teams_playing_today.append(away_team.abbreviation)
                        game_metrics, game_rules = self.get_rules_and_metrics(CONSTANTS.GAME_KEY)
                        games_today.append(Game(home_team, away_team, game_metrics, game_rules))
        return games_today
    
    def get_game_for_team(self, team_abbreviation):
        now_formatted = self.date_of_games.strftime("%m-%d-%Y")
        team_game = None
        game_found = False
        schedule = self.get_team_schedule(team_abbreviation)
        if (schedule):
            for game in schedule:
                if (not game_found):
                    date_time_obj = dateutil.parser.parse(game.date).strftime("%m-%d-%Y")
                    if (date_time_obj == now_formatted):
                        game_found = True
                        team_game = game
        return team_game

    def get_team_schedule(self, team_abbreviation):
        schedule = sports_objects.get_sport_object(self.league, CONSTANTS.SCHEDULE)
        if schedule:
            try:
                return schedule(team_abbreviation)
            except HTTPError:
                print(team_abbreviation + " does not have a schedule!")
                return None
        else:
            return None

    def get_teams(self, team_abbreviation=None, year=None):
        teams = sports_objects.get_sport_object(self.league, CONSTANTS.TEAMS)
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

    def get_team_roster(self, team_abbreviation, year, player_metrics, rules):
        roster = self.get_sports_reference_roster(team_abbreviation, year, False)
        modified_roster = []
        for player in roster.players:
            modified_roster.append(Player(player, player_metrics, rules))
        return modified_roster

    def get_sports_reference_roster(self, team_abbreviation, year, slim=False):
        roster = sports_objects.get_sport_object(self.league, CONSTANTS.ROSTER)
        if roster:
            try:
                return roster(team_abbreviation, year, slim)
            except HTTPError:
                print(team_abbreviation + " does not a roster!")
                return None
        else:
            return None

    def get_player(self, player_id):
        player = sports_objects.get_sport_object(self.league, CONSTANTS.PLAYER)
        if player:
            try:
                return player(player_id)
            except HTTPError:
                print(player_id + " does not exist!")
                return None
        else:
            return None
    
    def get_rules_and_metrics(self, type):
        metrics = None
        rules = None
        for logic in self.json_logic:
            object = logic.get(type)
            if object:
                metrics = object.get(CONSTANTS.METRICS_KEY)
                rules = object.get(CONSTANTS.RULES_KEY)
        return metrics, rules