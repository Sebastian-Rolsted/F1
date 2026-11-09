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
def driver_form():
    data = pd.read_csv(data_dir/'all_seasons.csv')
    data = data.sort_values(by=['season', 'round'], ascending=True)
    data['form_driver_3_races'] = data.groupby('driver')['finision_possion'].transform(lambda s: s.shift(1).rolling(3).mean())

    #Sampels the teams to the newest name name
    team_names = {
    'Force India': 'Aston Martin',
    'Racing Point': 'Aston Martin',
    'Toro Rosso': 'Racing Bulls',
    'AlphaTauri': 'Racing Bulls',
    'RB': 'Racing Bulls',
    'Sauber': 'Kick Sauber',
    'Alfa Romeo Racing': 'Kick Sauber',
    'Alfa Romeo': 'Kick Sauber',
    'Renault': 'Alpine',}
    data['team_newest_name'] = data['team'].replace(team_names)
    
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

    data.to_csv(data_dir/'all_seasons_features.csv')

    return data

test = driver_form()
