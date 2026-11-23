import glob
import os
import boto3
from botocore.exceptions import ClientError


def upload_healthcare_pipeline():
    s3_client = boto3.client('s3')

    BUCKET_NAME = "yt-healthcare-claim-fraud-leakage-pipeline-dpp-pidhya"
    S3_FOLDER = "daily_claims_exports"

    # 🔥 FIX: Use glob to find all CSV files inside the directory with their full paths
    search_path = os.path.join(S3_FOLDER, "*.csv")
    local_files = glob.glob(search_path)

    print(f" Found {len(local_files)} claims files to process.\n")

    for file_path in local_files:
        # Extract just the filename (e.g., raw_claims_20261025_sample.csv)
        filename = os.path.basename(file_path)

        # Construct the target path for S3
        s3_key = f"{S3_FOLDER}/{filename}"

        print(f"Uploading: {file_path} ➔ s3://{BUCKET_NAME}/{s3_key}...")

        try:
            # Pass the correct local path containing the folder prefix
            s3_client.upload_file(file_path, BUCKET_NAME, s3_key)
            print(f"✅ Successfully uploaded {filename}!\n")
        except ClientError as e:
            print(f"❌ AWS Cloud Error on {filename}: {e}\n")


if __name__ == "__main__":
    upload_healthcare_pipeline()
