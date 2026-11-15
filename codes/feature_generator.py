import fastf1
import pandas as pd
import numpy as np
from pathlib import Path


fastf1.set_log_level('ERROR')

data_dir = Path('/Users/Sebastian_Keller_Rolsted/ML_projekts/F1/data/')

#Recent form for the drivers
def driver_form(df):
    data = df
    data['form_driver_3_races'] = data.groupby('driver')['finision_possion'].transform(lambda s: s.shift(1).rolling(3).mean())

    return data

def team_form_and_track(df):
    data = df

    team_race = data.groupby(['team_newest_name', 'season', 'round', 'circuit'])['finision_possion'].mean().reset_index()
    team_race = team_race.rename(columns={'finision_possion': 'team_avg_pos'})
    team_race['team_rank'] = team_race.groupby(['season', 'round'])['team_avg_pos'].rank()
    
    team_race = team_race.sort_values(by=['season', 'round'], ascending=True)
    team_race['form_team_3_races'] = team_race.groupby('team_newest_name')['team_rank'].transform(lambda s: s.shift(1).rolling(3).mean())

    #Track history
    team_race['team_track_result'] = team_race.groupby(['team_newest_name', 'circuit'])['team_rank'].transform(lambda s: s.shift(1))
    #avg over 3 races
    team_race['team_avg3_track_result'] = team_race.groupby(['team_newest_name', 'circuit'])['team_rank'].transform(lambda s: s.shift(1).rolling(3, min_periods=2).mean())
    
    #Merge df
    data = pd.merge(
    data,
    team_race[['season', 'round', 'team_newest_name', 'form_team_3_races', 'team_track_result', 'team_avg3_track_result']],
    on=['season', 'round', 'team_newest_name'],how='left')

    #fill na
    data['team_track_result_filled'] = data['team_track_result'].fillna(data['form_team_3_races'])
    data['team_avg3_track_result_filled'] = data['team_avg3_track_result'].fillna(data['form_team_3_races'])    
    
    return data

#Track history
def track_history_driver(df):
    data = df

    #last result on the track
    data['track_result'] = data.groupby(['circuit', 'driver'])['finision_possion'].transform(lambda s: s.shift(1))
    #fill na
    data['track_result_filled'] = data['track_result'].fillna(data['form_driver_3_races'])
    #past tre races on the track
    data['track_avg3_result'] = data.groupby(['circuit', 'driver'])['finision_possion'].transform(lambda s: s.shift(1).rolling(3, min_periods=2).mean())
    #fill na
    data['track_avg3_result_filled'] = data['track_avg3_result'].fillna(data['form_driver_3_races'])
    
    return data


def main(save = False, verbose = False):
    if verbose:
        print('='*100)
        print('Starting the feature generating')
        print('='*100)
        print('='*20 +'Loding the data' +'='*20)
        print()
    data = pd.read_csv(data_dir/'all_seasons.csv')

    data = data.sort_values(by=['season', 'round'], ascending=True)
    if verbose:
        print('='*20 +'generating driver form' +'='*20)
    data = driver_form(data)
    if verbose:
        print('='*20 +'generating team form and track history' +'='*20)
    data = team_form_and_track(data)
    if verbose:
        print('='*20 +'generating driver track history' +'='*20)
    data = track_history_driver(data)

    if save:
        if verbose:
            print('='*20 +'saving file to: all_seasons_features.csv' +'='*20)
            print()
            
        data.to_csv(data_dir/'all_seasons_features.csv', index=False)
    if verbose:
        print('='*100)
        print('Done')
        print('='*100)

    return data

if __name__ == '__main__':
    data = main()
    print(data[(data['circuit'] == 'Silverstone') & (data['team_newest_name'] == 'McLaren')])



