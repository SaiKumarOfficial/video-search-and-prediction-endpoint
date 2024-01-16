from src.entity.config import AwsStorage
from boto3 import Session
import tarfile
import os


class StorageConnection:
    """
    Created connection with S3 bucket using boto3 api to fetch the model from Repository.
    """
    def __init__(self):
        self.config = AwsStorage()
        self.session = Session(aws_access_key_id=self.config.ACCESS_KEY_ID,
                               aws_secret_access_key=self.config.SECRET_KEY,
                               region_name=self.config.REGION_NAME)
        self.s3 = self.session.resource("s3")
        self.bucket = self.s3.Bucket(self.config.BUCKET_NAME)


    def get_package_from_testing(self):
        print("Fetching Artifacts From S3 Bucket .....")
        
        # List of files to remove
        files_to_remove = [
            "embeddings.ann",
            "model.pth",
            "embeddings.json"
        ]

        try:
            for file_to_remove in files_to_remove:
                file_path = os.path.join(self.config.ARTIFACTS_ROOT, file_to_remove)
                if os.path.exists(file_path):
                    os.remove(file_path)
        except Exception as e:
            print(f"Error removing file: {e}")

        try:
            os.makedirs(self.config.ARTIFACTS_ROOT, exist_ok=True)
        except Exception as e:
            print(f"Error creating directory: {e}")

        try:
            self.bucket.download_file(self.config.ZIP_NAME, self.config.ARTIFACTS_PATH)
            folder = tarfile.open(self.config.ARTIFACTS_PATH)
            folder.extractall(self.config.ARTIFACTS_ROOT)
            
            folder.close()
            os.chmod(self.config.ARTIFACTS_PATH, 0o777)  # Change file permissions to allow removal
            os.remove(self.config.ARTIFACTS_PATH)
            print("Fetching Completed !")
        except Exception as e:
            print(f"Error during download/extract: {e}")


if __name__ == "__main__":
    connection = StorageConnection()
    connection.get_package_from_testing()
