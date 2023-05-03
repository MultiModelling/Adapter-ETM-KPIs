'''
Singleton class containing the main Minio connection
'''
from io import BytesIO

from minio import Minio

from tno.esdl_add_etm_kpis_adapter.settings import EnvSettings
from tno.shared.log import get_logger

logger = get_logger(__name__)

class MinioConnection:

    class __MinioConnection:
        def __init__(self):
            self.minio_client = None
            if EnvSettings.minio_endpoint():
                logger.info(f"Connecting to Minio Object Store at {EnvSettings.minio_endpoint()}")
                self.minio_client = Minio(
                    endpoint=EnvSettings.minio_endpoint(),
                    secure=EnvSettings.minio_secure(),
                    access_key=EnvSettings.minio_access_key(),
                    secret_key=EnvSettings.minio_secret_key()
                )
            else:
                logger.info("No Minio Object Store configured")

        def connected(self):
            return True if self.minio_client else False

    instance = None
    def __init__(self):
        if not MinioConnection.instance:
            MinioConnection.instance = MinioConnection.__MinioConnection()

    def connected(self):
        self.instance.connected()

    def load_from_path(self, path):
        """
        Tries to load from minio
        TODO: let us know if it didn't work - not just return none silently
        """

        bucket = path.split("/")[0]
        rest_of_path = "/".join(path.split("/")[1:])

        response = self.instance.minio_client.get_object(bucket, rest_of_path)
        if response:
            return response.data
        else:
            return None

    def store_result(self, path, result) -> dict:
        """
        Stores the result if possible and returns the result dict that
        should be set on the model run result
        """
        if not self.connected():
            return {"result": result}

        content = BytesIO(bytes(result, 'ascii'))

        bucket = path.split("/")[0]
        rest_of_path = "/".join(path.split("/")[1:])

        if not self.instance.minio_client.bucket_exists(bucket):
            self.instance.minio_client.make_bucket(bucket)

        self.instance.minio_client.put_object(
            bucket, rest_of_path, content, content.getbuffer().nbytes
        )
        return {"path": path}
