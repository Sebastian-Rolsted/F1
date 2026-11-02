import fastf1
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns
from IPython.display import display as dp
from pathlib import Path


fastf1.set_log_level('ERROR')



### Load Data ###
def load_data(year):
    dir = Path('/Users/Sebastian_Keller_Rolsted/ML_projekts/F1/data/')
    df = pd.read_csv(dir / f'df_{year}.csv')
    return df

### The preditive model ###
def predict_winner_from_last(year, verbose = False):
    data = load_data(year)
    if verbose:
        print(f'The start of the funktion. The year is {year}.\n')
    correct = 0
    wrong = 0


    for n_round in range(1,data['round'].nunique() + 1):
        round_n = data[data['round'] == n_round].reset_index(drop=True)
        index = int(round_n.index[round_n["finision_possion"]==1][0])
        this_winner = str(round_n['driver'].iloc[index])

        if verbose:
            print(f'This is the {n_round} of {int(data["round"].nunique())} in {round_n["circuit"].iloc[index]}')
            print(f'The winner was {this_winner}')
        
        if n_round == 1:
            last_winner = this_winner
            if verbose:
                print('This was the first race and there were no last winner')
        else:
            if verbose:
                print(f'The last winner was {last_winner}')
            if this_winner == last_winner:
                if verbose:
                    print('It was a correct prediction\n')
                correct += 1
            else:
                if verbose:
                    print('It was wrong a wrong prediction\n')
                wrong += 1
            last_winner = this_winner

    return correct, wrong

def evaluation(*years, save=False, verbose = False):
    collumes = ['season', 'correct', 'wrong', 'total']
    df = pd.DataFrame(columns=collumes)
    for year in years:
        print(f'Season {year}')
        correct , wrong = predict_winner_from_last(year, verbose=verbose)
        total = correct + wrong
        append = {'season': year, 'correct': correct, 'wrong': wrong, 'total': total}
        df.loc[len(df)] = append

    df['correct_acc'] = round((df["correct"]/df["total"])*100, 2)
    mean_acc = round(df.correct_acc.mean(), 2)
    print(f'The mean accuracy is {mean_acc}.')

    if save:
        end_dir = Path("/Users/Sebastian_Keller_Rolsted/ML_projekts/F1/data")
        if len(years) > 1:
            df.to_csv(end_dir / f'evaluation{df["season"].min()}_{df["season"].max()}.csv', index=False)
        else:
            df.to_csv(end_dir / f'evaluation{df["season"].iloc[0]}.csv', index=False)
    return df


if __name__ == "__main__":
    print('Do you want to predict one or all year? (one or all)')
    prediction = input().lower()
    if prediction == 'one':
        print('What year do you want to predict?')
        year = int(input())
        
        print('Do you want to print? (y or n)')
        verbose = input().lower() == 'y'

        print(f'Do you want to save it? (y or n)')
        save = input().lower() == 'y'

        evaluation(year, save= save, verbose=verbose)

    elif prediction == 'all':
        print('You will predicte season 2018-2025.')

        print('Do you want to print? (y or n)')
        verbose = input().lower() == 'y'
        
        print(f'Do you want to save it? (y or n)')
        save = input().lower() == 'y'

        evaluation(*range(2018,2026), save= save, verbose=verbose)
    else:
        print('You did not use one of the options')
