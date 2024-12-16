from google.cloud import storage

client = storage.Client()

bucket_name = "lahman_data"
file_name = "lahman_1871-2023_csv/HallOfFameDataset_Timeseries.csv"
destination_blob_name = "combined/HallOfFameDataset_Timeseries.csv"

bucket = client.bucket(bucket_name)
blob = bucket.blob(destination_blob_name)
blob.upload_from_filename(file_name)

print(f"File {file_name} uploaded to {destination_blob_name}.")