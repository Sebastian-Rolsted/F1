import fastf1
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns
from IPython.display import display as dp
from fastf1.ergast import Ergast


fastf1.set_log_level('ERROR')


def find_wc_leader(year, n_round):
     sesson_n = Ergast()
     season = sesson_n.get_driver_standings(season=year,round= n_round - 1) 
     wc_leader = season.content[0].iloc[0].familyName
     return wc_leader


def find_this_winner(year, n_round):
    if n_round == 1:
         print('It is the first race and there is no last winner')
        
    else:
        race = fastf1.get_session(year, n_round, 'R')
        race.load(laps=False, telemetry=False, weather=False, messages=False)
        this_winner = race.results.LastName.iloc[0]
    return this_winner

def find_last_winner(year, n_round):
    race = fastf1.get_session(year, n_round - 1, 'R')
    race.load(laps=False, telemetry=False, weather=False, messages=False)
    last_winner = race.results.LastName.iloc[0]
    return last_winner

def predict(wc_leader, this_winner, last_winner):
    if (this_winner.lower() == wc_leader.lower()) or (this_winner.lower() == last_winner.lower()):
        print('It was a correct prediction\n')
        corret = 1
        wrong = 0
    else:
        print('It was wrong a wrong prediction\n')
        wrong = 1
        corret =0
    return corret, wrong

def main(year, n_round):
    print(f'You have selectede the {n_round} round of the {year} season.\n')
    if n_round == 1:
        print('First race and no prediction')
        return 0, 0

    wc_leader = find_wc_leader(year=year, n_round=n_round)
    this_winner = find_this_winner(year=year, n_round=n_round)
    last_winner = find_last_winner(year=year, n_round=n_round)
    print(f'For the {n_round} round, the WC leader is {wc_leader}, and the last winner were {last_winner}. The winner of the race is {this_winner}')

    corret, wrong = predict(wc_leader=wc_leader, this_winner=this_winner, last_winner=last_winner)
    if corret == 1:
         print(f'The model made a corret prediction')
    else:
         print(f'The prediction were wrong')
    return corret, wrong


def season_acc(year):
    rounds = 0
    correct_all = 0
    wrong_all = 0

    for i in fastf1.get_event_schedule(year).iloc:
        if i.EventFormat != 'testing':
            rounds += 1

    for n_round in range(1,rounds+1):
        corret, wrong = main(year=year, n_round=n_round)
        correct_all += corret
        wrong_all += wrong

    correct_acc = round((correct_all/(correct_all+wrong_all))*100, 2)
    
    print(f'This model were correct in {correct_acc}% of the cases')
    return correct_all, wrong_all


year = int(input('What year do you want a prediction from: '))
#round_n = int(input('What round of the year: '))

#corret, wrong = main(year=year, n_round=round_n)

corret, wrong = season_acc(year=year)



