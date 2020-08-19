from drs_client.models import AccessURL, DrsObject, PostDrsObject
from pydantic import BaseModel
import requests
import json


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
        if req:
            DrsObject(**req.json())  # validate icoming payload
        return req.json()


    def get_access_url(self, object_id, access_id):
        """TODO"""
        request_url = f"http://{self.url}/objects/{object_id}/access/{access_id}"
        req = requests.get(url=request_url)
        if req: 
            AccessURL(**req.json())  # validate incoming payload
        return req.json()


    def post_object(self, object_data):
        """TODO"""
        request_url = f"http://{self.url}/objects"
        PostDrsObject(**object_data)  # validate outgoing payload
        req = requests.post(url=request_url, json = object_data)
        # print(req)
        return req.json()


    def delete_object(self, object_id):
        """TODO"""
        request_url = f"http://{self.url}/objects/{object_id}"
        req = requests.delete(url=request_url)
        return req.json()
