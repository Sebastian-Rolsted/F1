import fastf1
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns
from IPython.display import display as dp
from fastf1.ergast import Ergast


fastf1.set_log_level('ERROR')


def wc_leader_prediction(year):

    sesson_n = Ergast()
    correct = 0
    wrong = 0
    rounds = 0
    for i in fastf1.get_event_schedule(year).iloc:
            if i.EventFormat != 'testing':
                rounds += 1

    for n_round in range(1,rounds+1):
            
            race = fastf1.get_session(year, n_round, 'R')
            race.load(laps=False, telemetry=False, weather=False, messages=False)
            this_winner = race.results.LastName.iloc[0]
    
            print(f'This is the {n_round} of {rounds} in {race.event.EventName}')
            print(f'The winner was {this_winner}')
            
            if race.event.RoundNumber == 1:
                print('This was the first race and there were no WC leader')
                
            else:
                season = sesson_n.get_driver_standings(season=year,round= n_round - 1)
                wc_leader = season.content[0].iloc[0].familyName

                print(f'The WC leader is {wc_leader}')
                if this_winner.lower() == wc_leader.lower():
                    print('It was a correct prediction\n')
                    correct += 1
                else:
                    print('It was wrong a wrong prediction\n')
                    wrong += 1
                
    
    correct_acc = round((correct/(correct+wrong))*100, 2)
    wrong_acc = round((wrong/(correct+wrong))*100,2)
    
    print(f'This model were correct in {correct_acc}% of the cases')
    return correct, wrong

corect, wrong = wc_leader_prediction(2025)