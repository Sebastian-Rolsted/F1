import fastf1
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns
from IPython.display import display as dp
from fastf1.ergast import Ergast
import time
from pathlib import Path

fastf1.set_log_level('ERROR')

end_dir = Path("/Users/Sebastian_Keller_Rolsted/ML_projekts/F1/data")
end_dir.mkdir(exist_ok=True)


def df_per_season(year):
    rounds = 0
    collumes = ['season', 'round', 'circuit', 'driver', 'team', 'start_possion', 'finision_possion']
    df = pd.DataFrame(columns=collumes)

    for i in fastf1.get_event_schedule(year).iloc:
            if i.EventFormat != 'testing':
                rounds += 1
    for n_round in range(1,rounds + 1):
        race = fastf1.get_session(year, n_round, 'R')
        race.load(laps=False, telemetry=False, weather=False, messages=False)
        event_name = race.event.Location

        for i in range(0,len(race.results)):
            if (pd.isna(race.results.GridPosition.iloc[i])) or (pd.isna(race.results.Position.iloc[i])):
                 continue
            f = race.results.FirstName.iloc[i]
            l = race.results.LastName.iloc[i]
            driver = f + ' ' + l

            append = {'season': year, 'round':n_round, 'circuit': event_name, 'driver': driver, 'team': race.results.TeamName.iloc[i] ,'start_possion': int(race.results.GridPosition.iloc[i]), 'finision_possion': int(race.results.Position.iloc[i])}
            df.loc[len(df)] = append

        print(f'Round {n_round} in {year} complitede')
        time.sleep(1)

    return df

#print('What year do you want to make a DataFrame about?')
#year = int(input())

#season_df = df_per_season(year=year)
#season_df.to_csv(end_dir / f'df_{year}.csv', index=False)



def load_data(year):
    dir = Path('/Users/Sebastian_Keller_Rolsted/ML_projekts/F1/data/')
    df = pd.read_csv(dir / f'df_{year}.csv')
    return df
def add_wc_leader():
    for year in range(2018,2026,1):
        print(year)
        data = load_data(year)
        time.sleep(2)
        data['wc_leader'] = 0
        for i in range(1, data['round'].nunique()+1):
            print(i)
            ergast = Ergast()
            round = ergast.get_driver_standings(season=year,round=i)
            wc_leader = round.content[0].givenName.iloc[0] + ' ' + round.content[0].familyName.iloc[0]
            

            data.loc[(data['round']== i+1) & (data['driver'] == wc_leader), 'wc_leader'] = 1
            time.sleep(1)
        data.to_csv(end_dir / f'df_{year}.csv', index=False)
