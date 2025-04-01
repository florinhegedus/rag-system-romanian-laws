import requests
from core.minio_client import MinIOClient
from core.legal_docs import LegalDocsEnum


class SavingUtilities:
    def __init__(self):
        """
        Initializes the SavingUtilities class.
        """
        self.links = [
            LegalDocsEnum.CODUL_PENAL,
            LegalDocsEnum.CODUL_DE_PROCEDURA_PENALA,
            LegalDocsEnum.CODUL_CIVIL,
            LegalDocsEnum.CODUL_DE_PROCEDURA_CIVILA,
            LegalDocsEnum.CODUL_FISCAL,
            LegalDocsEnum.CODUL_DE_PROCEDURA_FISCALA,
            LegalDocsEnum.CODUL_MUNCII
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
