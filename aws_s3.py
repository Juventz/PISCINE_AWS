import boto3
import os
from dotenv import load_dotenv

load_dotenv()

AWS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_KEY_ID,
    aws_secret_access_key=AWS_ACCESS_KEY
)


def upload_to_s3(file_path, bucket_name=AWS_BUCKET_NAME):

    file_name = os.path.basename(file_path)
    try:
        s3_client.upload_file(file_path, bucket_name, file_name)
        print(f"File uploaded successfully to {bucket_name}")
    except Exception as e:
        print(f"Error uploading file to {bucket_name}: {e}")


def list_s3_files(bucket_name=AWS_BUCKET_NAME):
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        if "Contents" in response:
            return [file["Key"] for file in response["Contents"]]
        else:
            return []
    except Exception as e:
        print(f"Error listing files in {bucket_name}: {e}")
        return []


def download_from_s3(file_name, save_path, bucket_name=AWS_BUCKET_NAME):
    try:
        s3_client.download_file(bucket_name, file_name, save_path)
        print(f"File downloaded successfully to {save_path}")
    except Exception as e:
        print(f"Error downloading file from {bucket_name}: {e}")


def delete_from_s3(file_name, bucket_name=AWS_BUCKET_NAME):
    try:
        s3_client.delete_object(Bucket=bucket_name, Key=file_name)
        print(f"File deleted successfully from {bucket_name}")
    except Exception as e:
        print(f"Error deleting file from {bucket_name}: {e}")


if __name__ == "__main__":
    log_file = "logs/app.log"

    # Upload file to S3
    upload_to_s3(log_file)

    # List files in S3
    files = list_s3_files()
    print(f"Files in S3: {files}")

    # Download file from S3
    if files:
        download_from_s3(files[0], f"downloads/{files[0]}")