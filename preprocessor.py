import pandas as pd

def preprocess(df, region_df):

    print(">>> Running preprocessor.py...")

    # Filter Summer Olympics
    df = df[df['Season'] == 'Summer']

    # Merge region info
    df = df.merge(region_df, on='NOC', how='left')

    # Drop duplicates for athletes in team events
    df.drop_duplicates(subset=['Year', 'Event', 'Name', 'Team'], inplace=True)

    # One-hot encode medals
    df = pd.concat([df, pd.get_dummies(df['Medal']).astype(int)], axis=1)
    df['Total'] = df[['Gold', 'Silver', 'Bronze']].sum(axis=1)

    return df
