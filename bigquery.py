from google.cloud import storage
import os

def copy_files_from_gcs_bucket(bucket_name, source_directory, destination_directory):
    # Initialize the Google Cloud Storage client
    client = storage.Client()

    # Get the GCS bucket
    bucket = client.get_bucket(bucket_name)

    # List all objects in the source directory
    blobs = bucket.list_blobs(prefix=source_directory)

    # Ensure the destination directory exists locally
    os.makedirs(destination_directory, exist_ok=True)

    # Copy each object from GCS to the local directory
    for blob in blobs:
        source_blob_name = blob.name
        destination_file_name = os.path.join(destination_directory, os.path.basename(source_blob_name))

        # Download the file from GCS to the local directory
        blob.download_to_filename(destination_file_name)

if __name__ == "__main__":
    # Replace with your GCS bucket name
    bucket_name = "your-bucket-name"

    # Replace with the source directory in the bucket (leave empty for the root)
    source_directory = "your/source/directory"

    # Replace with the local destination directory
    destination_directory = "path/to/local/destination"

    copy_files_from_gcs_bucket(bucket_name, source_directory, destination_directory)
    print("Files copied from GCS bucket to the local directory.")
