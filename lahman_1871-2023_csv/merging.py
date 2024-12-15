import pandas as pd

# Function to load CSV files and handle potential issues with encoding
def load_csv(file_path, encoding='utf-8'):
    try:
        return pd.read_csv(file_path, encoding=encoding)
    except UnicodeDecodeError:
        return pd.read_csv(file_path, encoding='latin1')

# File paths
file_paths = {
    'batting': 'lahman_1871-2023_csv/lahman_1871-2023_csv/Batting.csv',
    'pitching': 'lahman_1871-2023_csv/lahman_1871-2023_csv/Pitching.csv',
    'fielding': 'lahman_1871-2023_csv/lahman_1871-2023_csv/Fielding.csv',
    'awards': 'lahman_1871-2023_csv/lahman_1871-2023_csv/AwardsPlayers.csv',
    'hall_of_fame': 'lahman_1871-2023_csv/lahman_1871-2023_csv/HallOfFame.csv',
    'people': 'lahman_1871-2023_csv/lahman_1871-2023_csv/People.csv',
    # 'batting_post': 'lahman_1871-2023_csv/lahman_1871-2023_csv/BattingPost.csv',
    # 'pitching_post': 'lahman_1871-2023_csv/lahman_1871-2023_csv/PitchingPost.csv',
}

# Load all datasets
batting = load_csv(file_paths['batting'])
pitching = load_csv(file_paths['pitching'])
fielding = load_csv(file_paths['fielding'])
awards = load_csv(file_paths['awards'])
hof = load_csv(file_paths['hall_of_fame'])
people = load_csv(file_paths['people'], encoding='latin1')
# batting_post = load_csv(file_paths['batting_post'])
# pitching_post = load_csv(file_paths['pitching_post'])

# Aggregate batting stats
batting_agg = batting.groupby('playerID').agg({
    'G': 'sum', 'AB': 'sum', 'R': 'sum', 'H': 'sum',
    '2B': 'sum', '3B': 'sum', 'HR': 'sum', 'RBI': 'sum',
    'BB': 'sum', 'SO': 'sum'
}).reset_index()

# Aggregate pitching stats
pitching_agg = pitching.groupby('playerID').agg({
    'W': 'sum', 'L': 'sum', 'G': 'sum', 'GS': 'sum',
    'CG': 'sum', 'SV': 'sum', 'SO': 'sum', 'ERA': 'mean'
}).reset_index()

# Aggregate fielding stats
fielding_agg = fielding.groupby('playerID').agg({
    'G': 'sum', 'PO': 'sum', 'A': 'sum', 'E': 'sum'
}).reset_index()

# Aggregate awards count
awards_agg = awards.groupby('playerID')['awardID'].count().reset_index()
awards_agg.rename(columns={'awardID': 'AwardsCount'}, inplace=True)

# Career duration from People.csv
people['debut'] = pd.to_datetime(people['debut'], errors='coerce')
people['finalGame'] = pd.to_datetime(people['finalGame'], errors='coerce')
people['CareerLength'] = (people['finalGame'] - people['debut']).dt.days / 365.25
people_agg = people[['playerID', 'CareerLength']]

# Merge datasets
data = batting_agg.merge(pitching_agg, on='playerID', how='outer')
data = data.merge(fielding_agg, on='playerID', how='outer')
data = data.merge(awards_agg, on='playerID', how='left')
data = data.merge(people_agg, on='playerID', how='left')
data = data.merge(hof[['playerID', 'inducted']], on='playerID', how='left')

# Replace NaNs with 0 for stats and convert HoF status to binary
data.fillna(0, inplace=True)
data['inducted'] = data['inducted'].apply(lambda x: 1 if x == 'Y' else 0)

# Save merged dataset
data.to_csv("lahman_1871-2023_csv/HallOfFameDataset.csv", index=False)

print(f"Combined dataset saved to lahman.")
