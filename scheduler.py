import os
import pytz
from datetime import datetime
import pandas as pd

from sportsbetanalyzer import CONSTANTS, sports_objects
import utils
import s3_helper

leagues = sports_objects.get_map().keys()
utc_now = pytz.utc.localize(datetime.utcnow())
now = utc_now.astimezone(pytz.timezone(os.environ.get("TIMEZONE")))

def upload_rosters_to_s3():
    print("Uploading rosters to s3..")
    years_back = int(os.environ.get("REVENGE_GAME_YEARS_BACK"))
    for league in leagues:
        # Dont get rosters for ncaab because there is not support for revenge games
        if league != CONSTANTS.NCAAB:
            for num_of_years in range(0, years_back + 1):
                year_to_check = now.year - num_of_years
                index_year = str(year_to_check - 1) + "-" + str(year_to_check)[-2:]
                teams = utils.get_teams(league, None, year_to_check)
                for team in teams:
                    file_name = os.environ.get("TEMP_PICKLE_PATH") + "%s.pkl" % team.abbreviation.lower()
                    player_dataframes = []
                    if team and team.roster and team.roster.players:
                        for player in team.roster.players:
                            # This try catch is currently needed due to an issue with the sportsreference api
                            # getting the following error: AttributeError: 'NoneType' object has no attribute 'replace'
                            # when getting a player dataframe for nhl
                            try:
                                if player and player.dataframe is not None and not player.dataframe.empty:
                                    if index_year in player.dataframe.index:
                                        player_dataframe = player.dataframe.loc[index_year]
                                        player_dataframe["name"] = player.name
                                        player_dataframes.append(player_dataframe)
                            except:
                                print("Sportsreference error..")
                        if len(player_dataframes) > 0:
                            df = pd.concat(player_dataframes)
                            df["team_name"] = team.name
                            df.to_pickle(file_name)
                            s3_object_name = league + "/rosters/" + str(year_to_check) + "/" + "%s.pkl" % team.abbreviation.lower()
                            s3_helper.upload_file(file_name, os.environ.get("AWS_BUCKET_NAME"), s3_object_name)
                            print("Finished working on " + team.name)

def upload_schedules_to_s3():
    print("Uploading schedules to s3..")
    for league in leagues:
        teams = utils.get_teams(league, None, now.year)
        for team in teams:
            schedule = utils.get_team_schedule(league, team.abbreviation)
            file_name = os.environ.get("TEMP_PICKLE_PATH") + "%s.pkl" % team.abbreviation.lower()
            if schedule and not schedule.dataframe.empty:
                schedule.dataframe.to_pickle(file_name)
                s3_object_name = league + "/schedules/" + "%s.pkl" % team.abbreviation.lower()
                s3_helper.upload_file(file_name, os.environ.get("AWS_BUCKET_NAME"), s3_object_name)
                print("Finished working on " + team.name)