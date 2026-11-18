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
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from baseline_model import evaluation as eval_last_winner
from wc_leader_predict import evaluation as eval_wc_leader


fastf1.set_log_level('ERROR')

### Set up ###
data_dir = Path('/Users/Sebastian_Keller_Rolsted/ML_projekts/F1/data/')

features = ['wc_leader', 'win_last_race',
            'form_driver_3_races', 'form_team_3_races',
            'track_result_filled', 'track_avg3_result_filled',
            'team_track_result_filled',
            'last_race', 'driver_vs_team', 'driver_vs_team_avg3', 'team_form_vs_previerions_form']
outcome = 'winner'



def prepare_data(validation_year = 2024):
    data = pd.read_csv(data_dir / 'all_seasons_features.csv')
    data['winner'] = np.where(data['finision_possion'] == 1, 1,0)
    data['split'] = np.where(data['season'] < validation_year, 'train', np.where(data['season']== validation_year, 'val', 'test'))

    return data


def model_setup(class_weight = None):
    preprocess = Pipeline([('imputer', SimpleImputer(strategy='median')), ('scaler', StandardScaler())])
    pipeline = Pipeline([('preprocess', preprocess), ('model', LogisticRegression(max_iter=1000, class_weight=class_weight))])       

    return pipeline

def train_model(df, class_weight = None):
    data = df
    pipeline = model_setup(class_weight=class_weight)
    train = data[data['split'] == 'train']
    
    pipeline.fit(train[features], train[outcome])

    return pipeline

def add_predictions(model, data):
    data = data.copy()
    train = data[data['split'] == 'train']
    val = data[data['split'] == 'val']

    is_train = data['split'] == 'train'
    is_val = data['split'] == 'val'


    data.loc[is_train, 'win_prob'] = model.predict_proba(train[features])[:,1]
    data.loc[is_val, 'win_prob'] = model.predict_proba(val[features])[:,1]

    return data


def model_scoring(data, split):
    df_split = data[data['split'] == split]

    idx = df_split.groupby(['season', 'round'])['win_prob'].idxmax()
    
    model_winner_picks = df_split.loc[idx]

    return model_winner_picks['winner'].mean(), model_winner_picks


if __name__ == '__main__':
    print('='*100)
    print('Starting the setup of the model')
    print('='*100)

#    data = prepare_data()

    versions = {'scaled': {'class_weight': None},
                'class weight and scalede': {'class_weight': 'balanced'}}
    validation_yeres = [2022, 2023, 2024]

    model_performance = []
    for year in validation_yeres:
        print('='*100)
        print(year)
        print('='*100)
        data = prepare_data(validation_year=year)
        for name, setting in versions.items():
            model = train_model(data, class_weight=setting['class_weight'])
            df = add_predictions(model, data)

            print('='*30, name, '='*30)
            train_acc = 0
            val_acc = 0
            for split in ['train', 'val']:
                acc, picks = model_scoring(df, split=split)
                print(f'{split}: {acc:.1%}')
                if split == 'train':
                    train_acc = acc
                else:
                    val_acc = acc
                print()
            print('model coefs:')
            coefs = pd.Series(model.named_steps['model'].coef_[0], index=features).sort_values()
            print(coefs)
            print()
            print(model.named_steps['model'].class_weight)
            last_winner_df = eval_last_winner(year)
            last_winner_acc = last_winner_df['correct_acc'].iloc[0]/100
            wc_leader_df = eval_wc_leader(year)
            wc_leader_acc =   wc_leader_df['correct_acc'].iloc[0]/100
            performance = {'year': year, 'versions':name, 'train_acc': train_acc, 'val_acc': val_acc, 'last_winner': last_winner_acc, 'wc_leader': wc_leader_acc}
            model_performance.append(performance)

    performance_df = pd.DataFrame(model_performance)
    performance_df.to_csv(data_dir/'model_validation.csv', index=False)
    print(performance_df)
    

    data = prepare_data()
    model = train_model(data)
    df = add_predictions(model, data)

    df.to_csv(data_dir/'model_data.csv', index=False)




