import pandas as pd


matches = pd.read_csv('matches.csv')
deliveries = pd.read_csv('deliveries.csv')

print("Original Deliveries:", deliveries.shape)
print("Original Matches:", matches.shape)


total_scores = deliveries.groupby(['match_id', 'inning']).sum()['total_runs'].reset_index()

target_df = total_scores[total_scores['inning'] == 1]
target_df['total_runs'] = target_df['total_runs'] + 1

match_df = matches.merge(target_df[['match_id', 'total_runs']], left_on='id', right_on='match_id')

match_df = match_df.rename(columns={'total_runs': 'target'})


teams = [
    'Sunrisers Hyderabad', 'Mumbai Indians', 'Royal Challengers Bangalore',
    'Kolkata Knight Riders', 'Kings XI Punjab', 'Chennai Super Kings',
    'Rajasthan Royals', 'Delhi Capitals'
]

match_df['team1'] = match_df['team1'].str.replace('Delhi Daredevils', 'Delhi Capitals')
match_df['team2'] = match_df['team2'].str.replace('Delhi Daredevils', 'Delhi Capitals')
match_df['team1'] = match_df['team1'].str.replace('Deccan Chargers', 'Sunrisers Hyderabad')
match_df['team2'] = match_df['team2'].str.replace('Deccan Chargers', 'Sunrisers Hyderabad')

match_df = match_df[match_df['team1'].isin(teams)]
match_df = match_df[match_df['team2'].isin(teams)]

match_df = match_df[['id', 'city', 'winner', 'target']] 
delivery_df = match_df.merge(deliveries, left_on='id', right_on='match_id')

delivery_df = delivery_df[delivery_df['inning'] == 2]

#Calculate Score, Runs Left and Balls Left
delivery_df['current_score'] = delivery_df.groupby('match_id')['total_runs'].cumsum()
delivery_df['runs_left'] = delivery_df['target'] - delivery_df['current_score']
delivery_df['balls_left'] = 126 - (delivery_df['over']*6 + delivery_df['ball'])

#Calculate Wickets left
# Using 0s and 1s
delivery_df['player_dismissed'] = delivery_df['player_dismissed'].fillna("0")
delivery_df['player_dismissed'] = delivery_df['player_dismissed'].apply(lambda x: "0" if x=="0" else "1")
delivery_df['player_dismissed'] = delivery_df['player_dismissed'].astype('int')

wickets = delivery_df.groupby('match_id')['player_dismissed'].cumsum()
delivery_df['wickets'] =  10 - wickets

#Calculating the CRR
delivery_df['crr'] = (delivery_df['current_score']*6) / (120-delivery_df['balls_left'])

#Calculating the RRR (Required Run Rate)
delivery_df['rrr'] = (delivery_df['runs_left']*6) / delivery_df['balls_left']

#The Result using 1 if Batting Team wins else 0
def result(row):
    return 1 if row['batting_team'] == row['winner'] else 0

delivery_df['result'] = delivery_df.apply(result,axis=1)

final_df = delivery_df[['batting_team', 'bowling_team', 'city', 'runs_left', 'balls_left', 'wickets','target','crr','rrr','result']]

# Drop impossible values (e.g. balls_left = 0 which causes infinity errors)
final_df = final_df.sample(final_df.shape[0]) # Shuffle rows so the AI doesn't memorize match order
final_df.dropna(inplace=True) # Remove rows with missing values
final_df = final_df[final_df['balls_left'] != 0] # Avoid division by zero errors

# 17. Save to CSV
final_df.to_csv('final_dataset.csv', index=False)
print("--- SUCCESS: 'final_dataset.csv' created ---")
print(final_df.head())