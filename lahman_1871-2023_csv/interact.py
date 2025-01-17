# Interacting with GCP model

from google.cloud import aiplatform
import os
import dotenv

project = os.getenv("PROJECT_ID")
location = os.getenv("LOCATION")  # e.g., "us-central1"
endpoint_id = os.getenv("ENDPOINT_ID")  # From Vertex AI Console

client = aiplatform.gapic.PredictionServiceClient()

# Define endpoint
endpoint = f"projects/{project}/locations/{location}/endpoints/{endpoint_id}"

# Example prediction request
instances = [
    {"feature1": 0.5, "feature2": 1.2}  # Replace with your model's input format
]

response = client.predict(endpoint=endpoint, instances=instances)
print(response.predictions)
