import os
import pytz
from datetime import datetime
import pandas as pd

from sportsbetanalyzer import sports_objects
import utils
import s3_helper

leagues = sports_objects.get_map().keys()
utc_now = pytz.utc.localize(datetime.utcnow())
now = utc_now.astimezone(pytz.timezone(os.environ.get("TIMEZONE")))

def upload_rosters_to_s3():
    years_back = int(os.environ.get("REVENGE_GAME_YEARS_BACK"))
    for league in leagues:
        for num_of_years in range(0, years_back + 1):
            year_to_check = now.year - num_of_years
            index_year = str(year_to_check - 1) + "-" + str(year_to_check)[-2:]
            teams = utils.get_teams(league, None, year_to_check)
            for team in teams:
                file_name = os.environ.get("TEMP_PICKLE_PATH") + "%s.pkl" % team.abbreviation.lower()
                player_dataframes = []
                for player in team.roster.players:
                    if index_year in player.dataframe.index:
                        player_dataframe = player.dataframe.loc[index_year]
                        player_dataframe["name"] = player.name
                        player_dataframes.append(player_dataframe)
                df = pd.concat(player_dataframes)
                df["team_name"] = team.name
                df.to_pickle(file_name)
                s3_object_name = league + "/rosters/" + str(year_to_check) + "/" + "%s.pkl" % team.abbreviation.lower()
                s3_helper.upload_file(file_name, os.environ.get("AWS_BUCKET_NAME"), s3_object_name)
                print("Finished working on " + team.name)

def upload_schedules_to_s3():
    for league in leagues:
        teams = utils.get_teams(league, None, now.year)
        for team in teams:
            schedule = utils.get_team_schedule(league, team.abbreviation)
            file_name = os.environ.get("TEMP_PICKLE_PATH") + "%s.pkl" % team.abbreviation.lower()
            schedule.dataframe.to_pickle(file_name)
            s3_object_name = league + "/schedules/" + "%s.pkl" % team.abbreviation.lower()
            s3_helper.upload_file(file_name, os.environ.get("AWS_BUCKET_NAME"), s3_object_name)
            print("Finished working on " + team.name)