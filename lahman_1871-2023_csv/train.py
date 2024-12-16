import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from joblib import dump
from google.cloud import storage
import os

# Load the Lahman dataset
data = pd.read_csv("lahman_1871-2023_csv/HallOfFameDataset_Timeseries.csv")

# Define the specific features to be used
feature_columns = [
    'BattingGames', 'AtBats', 'Runs', 'Hits', 'Doubles', 'Triples', 'HomeRuns', 'RBIs', 'Walks', 'Strikeouts',
    'Wins', 'Losses', 'PitchingGames', 'GamesStarted', 'CompleteGames', 'Saves', 'PitchingStrikeouts', 'EarnedRunAverage',
    'FieldingGames', 'Putouts', 'Assists', 'Errors', 'AwardsCount'
]

# Define features and labels
features = data[feature_columns]
labels = data['inducted']

# Split the data into training and test sets
from sklearn.model_selection import train_test_split
train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.2, random_state=42)

# Define and train the Scikit model
skmodel = DecisionTreeClassifier()
skmodel.fit(train_features, train_labels)
score = skmodel.score(test_features, test_labels)
print('accuracy is:', score)

# Save the model to a local file
dump(skmodel, "model.joblib")

# # Upload the saved model file to GCS
# storage_client = storage.Client()
# bucket = storage_client.get_bucket("YOUR_GCS_BUCKET")
# model_directory = os.environ["AIP_MODEL_DIR"]
# storage_path = os.path.join(model_directory, "model.joblib")
# blob = storage.blob.Blob.from_string(storage_path, client=storage_client)
# blob.upload_from_filename("model.joblib")