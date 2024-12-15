import pandas as pd

# Load the batting and pitching CSV files
batting_df = pd.read_csv('lahman_1871-2023_csv/lahman_1871-2023_csv/Batting.csv')
pitching_df = pd.read_csv('lahman_1871-2023_csv/lahman_1871-2023_csv/Pitching.csv')

# Merge the DataFrames on the playerID column
combined_df = pd.merge(batting_df, pitching_df, on='playerID', how='outer')

# Save the combined DataFrame to a new CSV file
combined_df.to_csv('Combined_Batting_Pitching.csv', index=False)