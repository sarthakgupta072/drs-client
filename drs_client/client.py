from drs_client.models import AccessURL, DrsObject, PostDrsObject
from pydantic import BaseModel
import requests
import json


class DRSClient():
    """Client to communicate with a GA4GH DRS instance.
    Supports additional endpoints defined in DRS-filer (add URL).

    Args:
        host: Base URL of DRS instance.
        port: Port at which DRS instance can be accessed.
        base-path: Path at which DRS endpoints can be accessed.
    
    Attributes:
        url: URL to DRS endpoints, composed of `host`, `port` and `base_path`,
            e.g.,"https://my-drs.app:8080/ga4gh/drs/v1"
    """

    def __init__(
        self, 
        host= '0.0.0.0', 
        port = '80', 
        base_path= 'ga4gh/drs/v1'
    ) -> None:
        self.url = f"http://{host}:{port}/{base_path}"

    def get_object(self, object_id):
        """ Gets the DRS object

        Args:
            object_id: Identifier of DRS object to be retrieved.

        Returns:
            DRS object as dictionary, JSONified if returned in app context.
        """
        request_url = f"{self.url}/objects/{object_id}"
        req = requests.get(url=request_url)
        if req:
            DrsObject(**req.json())  # validate icoming payload
        return req.json()


    def get_access_url(self, object_id, access_id):
        """ Get access URL of DRS object.
        
        Args:
            object_id: Identifier of DRS object to be retrieved.
            access_id: Identifier of method giving access to DRS object.

        Returns:
            Object with access information for DRS object, containing a URL and
            any relevant header information; response is JSONified if returned in
            app context.
        """
        request_url = f"{self.url}/objects/{object_id}/access/{access_id}"
        req = requests.get(url=request_url)
        if req: 
            AccessURL(**req.json())  # validate incoming payload
        return req.json()


    def post_object(self, object_data):
        """ Register new DRS object.

        Args:
            object_data: DRS object in JSON form

        Returns:
            `object_id` of the registered DRS object
        """
        request_url = f"{self.url}/objects"
        PostDrsObject(**object_data)  # validate outgoing payload
        req = requests.post(url=request_url, json = object_data)
        # print(req)
        return req.json()


    def delete_object(self, object_id):
        """ Delete DRS object.
        
        Args:
            object_id: Identifier of DRS object to be deleted.

        Returns:
            `object_id` of deleted object.
        """
        request_url = f"{self.url}/objects/{object_id}"
        req = requests.delete(url=request_url)
        return req.json()
