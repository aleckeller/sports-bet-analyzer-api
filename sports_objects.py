from sportsreference.nba.teams import Teams as NBATeams
from sportsreference.nba.schedule import Schedule as NBASchedule
from sportsreference.nba.roster import Roster as NBARoster
from sportsreference.nba.roster import Player as NBAPlayer

from sportsreference.nhl.teams import Teams as NHLTeams
from sportsreference.nhl.schedule import Schedule as NHLSchedule
from sportsreference.nhl.roster import Roster as NHLRoster
from sportsreference.nhl.roster import Player as NHLPlayer

import CONSTANTS

def get_map():
    sports_map = {
        CONSTANTS.NBA : {
            CONSTANTS.TEAMS : NBATeams,
            CONSTANTS.SCHEDULE : NBASchedule,
            CONSTANTS.ROSTER : NBARoster,
            CONSTANTS.PLAYER : NBAPlayer
        },
        CONSTANTS.NHL : {
            CONSTANTS.TEAMS : NHLTeams,
            CONSTANTS.SCHEDULE : NHLSchedule,
            CONSTANTS.ROSTER : NHLRoster,
            CONSTANTS.PLAYER : NHLPlayer
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