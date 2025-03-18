import os
import requests
import boto3
from botocore.client import Config
from enum import Enum
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


class LegalDocEnum(Enum):
    CODUL_PENAL = "https://legislatie.just.ro/Public/DetaliiDocument/109855"
    CODUL_DE_PROCEDURA_PENALA = "https://legislatie.just.ro/Public/DetaliiDocument/120611"
    CODUL_CIVIL = "https://legislatie.just.ro/Public/DetaliiDocument/109884"
    CODUL_DE_PROCEDURA_CIVILA = "https://legislatie.just.ro/Public/DetaliiDocument/140271"
    CODUL_FISCAL = "https://legislatie.just.ro/Public/DetaliiDocument/171282"
    CODUL_DE_PROCEDURA_FISCALA = "https://legislatie.just.ro/Public/DetaliiDocument/172697"
    CODUL_MUNCII = "https://legislatie.just.ro/Public/DetaliiDocument/128647"


class MinIOClient:
    def __init__(self):
        """
        Initializes the MinIO client.
        """
        self.client = boto3.client(
            's3',
            endpoint_url='http://minio:9000',
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
            print(f"Bucket '{bucket_name}' already exists.")
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


class SavingUtilities:
    def __init__(self):
        """
        Initializes the SavingUtilities class.
        """
        self.links = [
            LegalDocEnum.CODUL_PENAL,
            LegalDocEnum.CODUL_DE_PROCEDURA_PENALA,
            LegalDocEnum.CODUL_CIVIL,
            LegalDocEnum.CODUL_DE_PROCEDURA_CIVILA,
            LegalDocEnum.CODUL_FISCAL,
            LegalDocEnum.CODUL_DE_PROCEDURA_FISCALA,
            LegalDocEnum.CODUL_MUNCII
        ]
        self.minio_client = MinIOClient()
        self.bucket_name = "legal-docs-minio-bucket"
    
    def save_page_content(self, link, filename):
        """
        Saves the content of a page to MinIO.
        """
        page = requests.get(link)

        self.minio_client.create_bucket_if_not_exists(self.bucket_name)
        self.minio_client.put_object(
            self.bucket_name, filename, page.content, len(page.content), content_type="text/html"
        )


def main():
    """
    Main function that collects data.
    """
    doc_saver = SavingUtilities()
    for link in doc_saver.links:
        doc_saver.save_page_content(link.value, f"{link.name}.html")
    doc_saver.minio_client.client.list_buckets()

    print("Data collection completed.")


if __name__ == '__main__':
    main()
