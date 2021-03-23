from datetime import datetime
import os
import pickle

from sportsbetanalyzer.Game import Game
from sportsbetanalyzer.Player import Player
from sportsbetanalyzer.Team import Team
import sportsbetanalyzer.CONSTANTS as CONSTANTS
from sportsbetanalyzer.OddsAPI import OddsAPI
import utils
import s3_helper

class GameGenerator:
    def __init__(self, league: str, date_of_games: datetime, json_logic: object):
        self.league = league
        self.date_of_games = date_of_games
        self.json_logic = json_logic
    
    def get_games(self, include_odds=True):
        if include_odds:
            odds_api_client = OddsAPI(self.league, os.environ.get("ODDS_API_KEY"))
            games_with_odds = odds_api_client.get_games_with_odds()
        teams = self.get_teams(year=self.date_of_games.year)
        teams_playing_today = []
        games_today = []
        for team in teams:
            if (team.abbreviation not in teams_playing_today):
                game = self.get_game_for_team(team.abbreviation)
                if (not game.empty):
                    opponent_abbreviation = game["opponent_abbr"].values[0].lower()
                    game_location = game["location"].values[0]
                    opponent_team = next((team for team in teams if team.abbreviation == opponent_abbreviation), None)
                    if game_location == CONSTANTS.HOME:
                        home_team = team
                        away_team = opponent_team
                    else:
                        home_team = opponent_team
                        away_team = team
                    teams_playing_today.append(home_team.abbreviation)
                    teams_playing_today.append(away_team.abbreviation)
                    game_metrics, game_rules = self.get_rules_and_metrics(CONSTANTS.GAME_KEY)
                    game_odds = {}
                    home_team_clean_key = utils.clean_key(home_team.name)
                    away_team_clean_key = utils.clean_key(away_team.name)
                    if include_odds:
                        for key, value in games_with_odds.items():
                            clean_key = utils.clean_key(key)
                            if self.league != CONSTANTS.NCAAB:
                                game_key = home_team_clean_key + away_team_clean_key
                                if game_key in clean_key or utils.shorten_state(game_key) in clean_key:
                                    game_odds = value
                            else:
                                if (home_team_clean_key in clean_key or 
                                        away_team_clean_key in clean_key or
                                        utils.shorten_state(home_team_clean_key) in clean_key or
                                        utils.shorten_state(away_team_clean_key) in clean_key):
                                        game_odds = value
                    games_today.append(Game(home_team, away_team, game_metrics, game_rules, game_odds))

        return games_today
    
    def get_game_for_team(self, team_abbreviation):
        now_formatted = self.date_of_games.strftime("%Y-%m-%d")
        schedule_key = self.league + "/schedules/" + team_abbreviation.lower() + ".pkl"
        file_contents = s3_helper.read_s3_object(os.environ.get("AWS_BUCKET_NAME"), schedule_key)
        team_schedule_df = pickle.loads(file_contents)
        game = team_schedule_df.loc[team_schedule_df['datetime'] == now_formatted]
        return game

    def get_teams(self, year=None):
        teams = []
        s3_objects = s3_helper.list_s3_objects(os.environ.get("AWS_BUCKET_NAME"), self.league + "/rosters/" + str(year) + "/")
        for s3_object in s3_objects["Contents"]:
            file_name = s3_object["Key"]
            file_contents = s3_helper.read_s3_object(os.environ.get("AWS_BUCKET_NAME"), file_name)
            team_dataframe = pickle.loads(file_contents)
            team_name = team_dataframe.iloc[0]["team_name"]
            team_abbreviation = file_name.split("/")[-1].replace(".pkl", "")
            player_metrics, player_rules = self.get_rules_and_metrics(CONSTANTS.PLAYER_KEY)
            team_roster = []
            for index, player_data in team_dataframe.iterrows():
                player_id = player_data["player_id"]
                name = player_data["name"]
                player = Player(player_id, name, player_metrics, player_rules, player_data)
                team_roster.append(player)
            
            team_metrics, team_rules = self.get_rules_and_metrics(CONSTANTS.TEAM_KEY)
            team = Team(team_name, team_abbreviation, team_metrics, team_roster, team_rules)
            teams.append(team)
        return teams
    
    def get_rules_and_metrics(self, type):
        metrics = None
        rules = None
        for logic in self.json_logic:
            object = logic.get(type)
            if object:
                metrics = object.get(CONSTANTS.METRICS_KEY)
                rules = object.get(CONSTANTS.RULES_KEY)
        return metrics, rules