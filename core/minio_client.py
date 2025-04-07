import os
import boto3
from botocore.client import Config
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()
 
# Set the endpoint URL based on the environment
if os.getenv("ENVIRONMENT") == "local":
    ENDPOINT_URL = 'http://localhost:9000'
else:
    ENDPOINT_URL = 'http://minio:9000'


class MinIOClient:
    def __init__(self):
        """
        Initializes the MinIO client.
        """
        self.client = boto3.client(
            's3',
            endpoint_url=ENDPOINT_URL,
            aws_access_key_id=os.getenv("MINIO_ROOT_USER"),
            aws_secret_access_key=os.getenv("MINIO_ROOT_PASSWORD"),
            config=Config(signature_version="s3v4")
        )

    def create_bucket_if_not_exists(self, bucket_name):
        """
        Creates a bucket if it does not exist.
        """
        try:
            self.client.head_bucket(Bucket=bucket_name)
        except self.client.exceptions.ClientError:
            self.client.create_bucket(Bucket=bucket_name)
            print(f"Bucket '{bucket_name}' created.")
    
    def put_object(self, bucket_name, object_name, data, length, content_type):
        """
        Uploads an object to a bucket.

        :param bucket_name: Name of the bucket.
        :param object_name: Name of the object (key) in the bucket.
        :param data: Data to upload (bytes or file-like object).
        :param length: Length of the data in bytes.
        :param content_type: Content type of the object (e.g., "text/plain").
        """
        try:
            self.client.put_object(
                Bucket=bucket_name,
                Key=object_name,
                Body=data,
                ContentLength=length,
                ContentType=content_type,
            )
            print(f"Object '{object_name}' uploaded to bucket '{bucket_name}'.")
        except Exception as e:
            print(f"Error uploading object: {e}")
    
    def get_object(self, bucket_name, object_name):
        """
        Retrieves an object from a bucket.

        :param bucket_name: Name of the bucket.
        :param object_name: Name of the object (key) in the bucket.
        :return: The content of the object as bytes.
        """
        try:
            response = self.client.get_object(Bucket=bucket_name, Key=object_name)
            return response['Body'].read()
        except Exception as e:
            print(f"Error retrieving object '{object_name}' from bucket '{bucket_name}': {e}")
            return None
