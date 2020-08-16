from drs_client.models import DrsObject
from pydantic import BaseModel
import requests


class DRSClient(BaseModel):
    """TODO"""
    host: str = '0.0.0.0'
    port: str = '8080'
    base_url: str = 'ga4gh/drs/v1'
    url = f"{host}:{port}/{base_url}"

    def get_object(self, object_id):
        """TODO"""
        request_url = f"http://{self.url}/objects/{object_id}"
        req = requests.get(url=request_url)
        obj = DrsObject(**req.json())
        return obj.json()


    def get_access_url(object_id, access_id):
        return None


    def post_object(object):
        return None


    def delete_object(object_id):
        return None
