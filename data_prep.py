import pandas as pd

# 1. Load the raw data
matches = pd.read_csv('matches.csv')
deliveries = pd.read_csv('deliveries.csv')

print("Original Deliveries:", deliveries.shape)
print("Original Matches:", matches.shape)

# 2. Calculate the Total Score for Every Inning
# NOTE: We use 'match_id' here because that is what it is called in deliveries.csv
total_scores = deliveries.groupby(['match_id', 'inning']).sum()['total_runs'].reset_index()

# 3. Filter for ONLY the 1st Innings score
target_df = total_scores[total_scores['inning'] == 1]

# 4. Add 1 to the score to create the "Target"
target_df['total_runs'] = target_df['total_runs'] + 1

# 5. Merge this Target info back into the Matches file
# CRITICAL FIX HERE:
# left_on='id'      <-- The name in matches.csv
# right_on='match_id' <-- The name in deliveries.csv
match_df = matches.merge(target_df[['match_id', 'total_runs']], left_on='id', right_on='match_id')

match_df = match_df.rename(columns={'total_runs': 'target'})

# 6. Filter matches to keep only valid games
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

# 7. The Big Merge: Connect Matches to Deliveries
# Again, handle the name mismatch
match_df = match_df[['id', 'city', 'winner', 'target']] 
delivery_df = match_df.merge(deliveries, left_on='id', right_on='match_id')

# 8. Focus on the CHASE (2nd Innings only)
delivery_df = delivery_df[delivery_df['inning'] == 2]

print("--- Data Ready ---")
print(delivery_df.shape)
print(delivery_df.head())