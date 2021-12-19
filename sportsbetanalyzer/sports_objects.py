from sportsbetanalyzer.sportsipy.nba.teams import Teams as NBATeams
from sportsbetanalyzer.sportsipy.nba.schedule import Schedule as NBASchedule
from sportsbetanalyzer.sportsipy.nba.roster import Roster as NBARoster
from sportsbetanalyzer.sportsipy.nba.roster import Player as NBAPlayer

from sportsbetanalyzer.sportsipy.nhl.teams import Teams as NHLTeams
from sportsbetanalyzer.sportsipy.nhl.schedule import Schedule as NHLSchedule
from sportsbetanalyzer.sportsipy.nhl.roster import Roster as NHLRoster
from sportsbetanalyzer.sportsipy.nhl.roster import Player as NHLPlayer

from sportsbetanalyzer.sportsipy.ncaab.teams import Teams as NCAABTeams
from sportsbetanalyzer.sportsipy.ncaab.schedule import Schedule as NCAABSchedule
from sportsbetanalyzer.sportsipy.ncaab.roster import Roster as NCAABRoster
from sportsbetanalyzer.sportsipy.ncaab.roster import Player as NCAABPlayer

from sportsbetanalyzer.sportsipy.mlb.teams import Teams as MLBTeams
from sportsbetanalyzer.sportsipy.mlb.schedule import Schedule as MLBSchedule
from sportsbetanalyzer.sportsipy.mlb.roster import Roster as MLBRoster
from sportsbetanalyzer.sportsipy.mlb.roster import Player as MLBPlayer

from sportsbetanalyzer.sportsipy.nfl.teams import Teams as NFLTeams
from sportsbetanalyzer.sportsipy.nfl.schedule import Schedule as NFLSchedule
from sportsbetanalyzer.sportsipy.nfl.roster import Roster as NFLRoster
from sportsbetanalyzer.sportsipy.nfl.roster import Player as NFLPlayer

import sportsbetanalyzer.CONSTANTS as CONSTANTS

def get_map():
    sports_map = {
        CONSTANTS.MLB : {
            CONSTANTS.TEAMS : MLBTeams,
            CONSTANTS.SCHEDULE : MLBSchedule,
            CONSTANTS.ROSTER : MLBRoster,
            CONSTANTS.PLAYER : MLBPlayer,
            CONSTANTS.ODDS_API_SPORTS_KEY : "baseball_mlb",
            CONSTANTS.POINTS_SCORED : "runs_scored",
            CONSTANTS.POINTS_ALLOWED : "runs_allowed"
        },
        CONSTANTS.NBA : {
            CONSTANTS.TEAMS : NBATeams,
            CONSTANTS.SCHEDULE : NBASchedule,
            CONSTANTS.ROSTER : NBARoster,
            CONSTANTS.PLAYER : NBAPlayer,
            CONSTANTS.ODDS_API_SPORTS_KEY : "basketball_nba",
            CONSTANTS.POINTS_SCORED : "points_scored",
            CONSTANTS.POINTS_ALLOWED : "points_allowed"
        },
        CONSTANTS.NHL : {
            CONSTANTS.TEAMS : NHLTeams,
            CONSTANTS.SCHEDULE : NHLSchedule,
            CONSTANTS.ROSTER : NHLRoster,
            CONSTANTS.PLAYER : NHLPlayer,
            CONSTANTS.ODDS_API_SPORTS_KEY : "icehockey_nhl",
            CONSTANTS.POINTS_SCORED : "goals_scored",
            CONSTANTS.POINTS_ALLOWED : "goals_allowed"
        },
        CONSTANTS.NCAAB : {
            CONSTANTS.TEAMS : NCAABTeams,
            CONSTANTS.SCHEDULE : NCAABSchedule,
            CONSTANTS.ROSTER : NCAABRoster,
            CONSTANTS.PLAYER : NCAABPlayer,
            CONSTANTS.ODDS_API_SPORTS_KEY : "basketball_ncaab",
            CONSTANTS.POINTS_SCORED : "points_scored",
            CONSTANTS.POINTS_ALLOWED : "points_allowed"
        },
        CONSTANTS.NFL : {
            CONSTANTS.TEAMS : NFLTeams,
            CONSTANTS.SCHEDULE : NFLSchedule,
            CONSTANTS.ROSTER : NFLRoster,
            CONSTANTS.PLAYER : NFLPlayer,
            CONSTANTS.ODDS_API_SPORTS_KEY : "americanfootball_nfl",
            CONSTANTS.POINTS_SCORED : "points_scored",
            CONSTANTS.POINTS_ALLOWED : "points_allowed"
        }
    }
    return sports_map

def get_sport_object(sport, object_type):
    sports_map = get_map()
    sport_object = None
    if sports_map.get(sport):
        if sports_map[sport].get(object_type):
            sport_object = sports_map[sport][object_type]
        else:
            raise Exception(object_type + " does not exist in " + sport + "!")
    else:
        raise Exception(sport + " does not exist!")
    return sport_object