import os

from minio import Minio

from ..settings import Settings


class Minio:
    def __init__(self, settings: Settings):
        self.bucket = settings.MINIO_BUCKET_NAME
        self.client = Minio(
            settings.MINIO_HOST,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=bool(settings.MINIO_SECURE),
        )

        if not self.client.bucket_exists(self.bucket):
            self.client.make_bucket(self.bucket)

    def download(
        self,
        path_file: str,
        path_save: str,
    ) -> str:
        """
        Download a file from Minio.
        :param path_file: Path of the file in Minio.
        :param path_save: Path to save the file.
        """

        self.client.fget_object(
            self.bucket,
            path_file,
            path_save,
        )

        return path_save

    def upload(
        self,
        path_file: str,
        filename: str,
        save_path: str,
        content_type: str,
    ) -> str:
        """
        Upload a file to Minio.
        :param path_file: Path of the file to upload.
        :param filename: Name of the file in Minio.
        :param save_path: Path to save the file in Minio.
        :param content_type: Content type of the file.
        """

        minio_path = os.path.join(save_path, filename)
        self.client.fput_object(
            self.bucket,
            minio_path,
            path_file,
            content_type=content_type,
        )
        return minio_path
