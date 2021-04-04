from sportsreference.nba.teams import Teams as NBATeams
from sportsreference.nba.schedule import Schedule as NBASchedule
from sportsreference.nba.roster import Roster as NBARoster
from sportsreference.nba.roster import Player as NBAPlayer

from sportsreference.nhl.teams import Teams as NHLTeams
from sportsreference.nhl.schedule import Schedule as NHLSchedule
from sportsreference.nhl.roster import Roster as NHLRoster
from sportsreference.nhl.roster import Player as NHLPlayer

from sportsreference.ncaab.teams import Teams as NCAABTeams
from sportsreference.ncaab.schedule import Schedule as NCAABSchedule
from sportsreference.ncaab.roster import Roster as NCAABRoster
from sportsreference.ncaab.roster import Player as NCAABPlayer

from sportsreference.mlb.teams import Teams as MLBTeams
from sportsreference.mlb.schedule import Schedule as MLBSchedule
from sportsreference.mlb.roster import Roster as MLBRoster
from sportsreference.mlb.roster import Player as MLBPlayer

import sportsbetanalyzer.CONSTANTS as CONSTANTS

def get_map():
    sports_map = {
        CONSTANTS.MLB : {
            CONSTANTS.TEAMS : MLBTeams,
            CONSTANTS.SCHEDULE : MLBSchedule,
            CONSTANTS.ROSTER : MLBRoster,
            CONSTANTS.PLAYER : MLBPlayer,
            CONSTANTS.ODDS_API_SPORTS_KEY : "baseball_mlb"
        },
        CONSTANTS.NBA : {
            CONSTANTS.TEAMS : NBATeams,
            CONSTANTS.SCHEDULE : NBASchedule,
            CONSTANTS.ROSTER : NBARoster,
            CONSTANTS.PLAYER : NBAPlayer,
            CONSTANTS.ODDS_API_SPORTS_KEY : "basketball_nba"
        },
        CONSTANTS.NHL : {
            CONSTANTS.TEAMS : NHLTeams,
            CONSTANTS.SCHEDULE : NHLSchedule,
            CONSTANTS.ROSTER : NHLRoster,
            CONSTANTS.PLAYER : NHLPlayer,
            CONSTANTS.ODDS_API_SPORTS_KEY : "icehockey_nhl"
        },
        CONSTANTS.NCAAB : {
            CONSTANTS.TEAMS : NCAABTeams,
            CONSTANTS.SCHEDULE : NCAABSchedule,
            CONSTANTS.ROSTER : NCAABRoster,
            CONSTANTS.PLAYER : NCAABPlayer,
            CONSTANTS.ODDS_API_SPORTS_KEY : "basketball_ncaab"
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