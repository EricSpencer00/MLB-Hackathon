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
}

# Load all datasets
batting_df = load_csv(file_paths['batting'])
pitching_df = load_csv(file_paths['pitching'])
fielding_df = load_csv(file_paths['fielding'])
awards_df = load_csv(file_paths['awards'])
hall_of_fame_df = load_csv(file_paths['hall_of_fame'])
people_df = load_csv(file_paths['people'], encoding='latin1')

# Merge batting and pitching stats
batting_pitching_df = pd.merge(
    batting_df, pitching_df,
    on=['playerID', 'yearID'],
    how='outer',
    suffixes=('_bat', '_pit')
)

# Identify columns common for merging fielding stats
common_columns = list(set(batting_pitching_df.columns) & set(fielding_df.columns))
required_columns = ['playerID', 'yearID']
additional_columns = ['teamID', 'lgID']
merge_columns = [col for col in required_columns + additional_columns if col in common_columns]

# Merge fielding stats carefully
batting_pitching_fielding_df = pd.merge(
    batting_pitching_df, fielding_df,
    on=merge_columns,
    how='outer'
)

# Merge awards with careful checks
if 'playerID' in awards_df.columns and 'yearID' in awards_df.columns:
    batting_pitching_fielding_awards_df = pd.merge(
        batting_pitching_fielding_df, awards_df,
        on=['playerID', 'yearID'],
        how='outer'
    )
else:
    batting_pitching_fielding_awards_df = batting_pitching_fielding_df

# Merge Hall of Fame information
full_df = pd.merge(
    batting_pitching_fielding_awards_df, hall_of_fame_df,
    on='playerID',
    how='outer'
)

# Merge player demographics and bios
if 'playerID' in people_df.columns:
    full_df = pd.merge(full_df, people_df, on='playerID', how='outer')

# Feature engineering: Add calculated stats (handle zero or missing AB and IPouts)
full_df['batting_average'] = full_df['H'] / full_df['AB']
full_df['batting_average'] = full_df['batting_average'].fillna(0)  # Avoid NaNs
full_df['slugging_percentage'] = (
    (full_df['H'] + full_df['2B'] + 2 * full_df['3B'] + 3 * full_df['HR']) / full_df['AB']
)
full_df['slugging_percentage'] = full_df['slugging_percentage'].fillna(0)
full_df['on_base_percentage'] = (
    (full_df['H'] + full_df['BB'] + full_df['HBP']) /
    (full_df['AB'] + full_df['BB'] + full_df['HBP'] + full_df['SF'])
)
full_df['on_base_percentage'] = full_df['on_base_percentage'].fillna(0)
full_df['ERA'] = (full_df['ER'] * 9) / (full_df['IPouts'] / 3)
full_df['ERA'] = full_df['ERA'].fillna(0)

# Handle NaN values in remaining columns
full_df = full_df.fillna('')

# Optimize data types
for col in full_df.select_dtypes(include=['float64']).columns:
    full_df[col] = pd.to_numeric(full_df[col], downcast='float')
for col in full_df.select_dtypes(include=['int64']).columns:
    full_df[col] = pd.to_numeric(full_df[col], downcast='integer')

# Save the final combined DataFrame
output_file = 'lahman_1871-2023_csv/Combined_Baseball_Stats_Optimized.csv'
full_df.to_csv(output_file, index=False)

print(f"Combined dataset saved to {output_file}")
