import pandas as pd
from joblib import load

# Load the model from the file
model = load("model.joblib")

# Define the specific features to be used
feature_columns = [
    'BattingGames', 'AtBats', 'Runs', 'Hits', 'Doubles', 'Triples', 'HomeRuns', 'RBIs', 'Walks', 'Strikeouts',
    'Wins', 'Losses', 'PitchingGames', 'GamesStarted', 'CompleteGames', 'Saves', 'PitchingStrikeouts', 'EarnedRunAverage',
    'FieldingGames', 'Putouts', 'Assists', 'Errors', 'AwardsCount'
]

# Example player data for prediction
example_players_data = [
    {
        'BattingGames': 11, 'AtBats': 0, 'Runs': 0, 'Hits': 0, 'Doubles': 0, 'Triples': 0, 'HomeRuns': 0, 'RBIs': 0,
        'Walks': 0, 'Strikeouts': 0, 'Wins': 1, 'Losses': 0, 'PitchingGames': 11, 'GamesStarted': 0, 'CompleteGames': 0,
        'Saves': 0, 'PitchingStrikeouts': 5, 'EarnedRunAverage': 6.75, 'FieldingGames': 11, 'Putouts': 0, 'Assists': 0,
        'Errors': 0, 'AwardsCount': 0
    },
    {
        'BattingGames': 150, 'AtBats': 500, 'Runs': 80, 'Hits': 150, 'Doubles': 30, 'Triples': 5, 'HomeRuns': 20, 'RBIs': 90,
        'Walks': 60, 'Strikeouts': 100, 'Wins': 0, 'Losses': 0, 'PitchingGames': 0, 'GamesStarted': 0, 'CompleteGames': 0,
        'Saves': 0, 'PitchingStrikeouts': 0, 'EarnedRunAverage': 0.0, 'FieldingGames': 150, 'Putouts': 300, 'Assists': 50,
        'Errors': 10, 'AwardsCount': 3
    },
    {
        'BattingGames': 200, 'AtBats': 600, 'Runs': 100, 'Hits': 200, 'Doubles': 40, 'Triples': 10, 'HomeRuns': 30, 'RBIs': 120,
        'Walks': 80, 'Strikeouts': 90, 'Wins': 0, 'Losses': 0, 'PitchingGames': 0, 'GamesStarted': 0, 'CompleteGames': 0,
        'Saves': 0, 'PitchingStrikeouts': 0, 'EarnedRunAverage': 0.0, 'FieldingGames': 200, 'Putouts': 400, 'Assists': 60,
        'Errors': 5, 'AwardsCount': 5
    }
]

# Convert the example player data to a DataFrame and make predictions
for player_data in example_players_data:
    example_player_df = pd.DataFrame([player_data], columns=feature_columns)
    prediction = model.predict(example_player_df)
    print(f'Prediction for player data {player_data} (1 for inducted, 0 for not inducted):', prediction[0])