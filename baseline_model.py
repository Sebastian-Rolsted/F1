import fastf1
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns
from IPython.display import display as dp


fastf1.set_log_level('ERROR')

def last_winner_acc(year):
    print(f'The start of the funktion. The year is {year}.\n')
    rounds = 0
    correct = 0
    wrong = 0

    for i in fastf1.get_event_schedule(year).iloc:
        if i.EventFormat != 'testing':
            rounds += 1

    for round in range(1,rounds+1):
        
        race = fastf1.get_session(year, round, 'R')
        race.load(laps=False, telemetry=False, weather=False, messages=False)
        this_winner = race.results.LastName.iloc[0]

        print(f'This is the {round} of {rounds} in {race.event.EventName}')
        print(f'The winner was {this_winner}')
        
        if race.event.RoundNumber == 1:
            print('This was the first race and there were no last winner')
            last_winner = this_winner
        else:
            print(f'The last winner was {last_winner}')
            if this_winner == last_winner:
                print('It was a correct prediction\n')
                correct += 1
            else:
                print('It was wrong a wrong prediction\n')
                wrong += 1
            last_winner = this_winner

    correct_acc = round((correct/(correct+wrong))*100, 2)
    wrong_acc = round((wrong/(correct+wrong))*100,2)

    print(f'This model were correct in {correct_acc}% of the cases')
    return correct, wrong

correct, wrong = last_winner_acc(2025)
print(f'There were {correct} correct predctions and {wrong} wrong predictions')