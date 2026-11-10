import fastf1
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns
from IPython.display import display as dp
from fastf1.ergast import Ergast
import time
from pathlib import Path
from wc_leader_predict import load_data


fastf1.set_log_level('ERROR')

data_dir = Path('/Users/Sebastian_Keller_Rolsted/ML_projekts/F1/data/')

#Recent form for the drivers
def driver_form(df):
    data = df
    data = data.sort_values(by=['season', 'round'], ascending=True)
    data['form_driver_3_races'] = data.groupby('driver')['finision_possion'].transform(lambda s: s.shift(1).rolling(3).mean())
    
    team_race = data.groupby(['team_newest_name', 'season', 'round'])['finision_possion'].mean().reset_index()
    team_race = team_race.rename(columns={'finision_possion': 'team_avg_pos'})
    team_race['team_rank'] = team_race.groupby(['season', 'round'])['team_avg_pos'].rank()

    team_race = team_race.sort_values(by=['season', 'round'], ascending=True)
    team_race['form_team_3_races'] = team_race.groupby('team_newest_name')['team_rank'].transform(lambda s: s.shift(1).rolling(3).mean())

    #Merge df
    data = pd.merge(
    data,
    team_race[['season', 'round', 'team_newest_name', 'form_team_3_races']],
    on=['season', 'round', 'team_newest_name'],
    how='left')        

    return data


#Track history
def track_history(df):
    data = df

    #last result on the track
    data['track_result'] = data.groupby(['circuit', 'driver'])['finision_possion'].transform(lambda s: s.shift(1))
    #past tre races on the track
    data['track_avg3_result'] = data.groupby(['circuit', 'driver'])['finision_possion'].transform(lambda s: s.shift(1).rolling(3, min_periods=2).mean())

    #team last result on the track
    team = data.groupby(['team_newest_name', 'season', 'round', 'circuit'])['finision_possion'].mean().reset_index()
    team = team.rename(columns={'finision_possion': 'team_avg_pos'})
    team['team_rank'] = team.groupby(['circuit', 'season', 'round'])['team_avg_pos'].rank()
    team['team_track_result'] = team.groupby(['team_newest_name', 'circuit'])['team_rank'].transform(lambda s: s.shift(1))
    #avg over 3 races
    team['team_avg3_track_result'] = team.groupby(['team_newest_name', 'circuit'])['team_rank'].transform(lambda s: s.shift(1).rolling(3, min_periods=2).mean())

    #Merge the df
    data = pd.merge(
        data,
        team[['season', 'round', 'team_newest_name', 'team_track_result', 'team_avg3_track_result']],
        on=['season', 'round', 'team_newest_name'],
        how='left')
    
    return data

def save_to_csv():
    data = pd.read_csv(data_dir/'all_seasons.csv')
    data = driver_form(data)
    data = track_history(data)

    data.to_csv(data_dir/'all_seasons_features.csv', index=False)


data = pd.read_csv(data_dir/'all_seasons_features.csv')
data.info()


