


# File only for testing. Will be removed in the future commits

from requests.api import delete
from drs_client.client import DRSClient
import json

client = DRSClient()
# print(client.delete_object('t0ltnK'))
print(client.get_object("t0ltnK"))
# print(client.get_access_url("t0ltnK", "rsn.dn"))
# with open('drs_client/test_data.json') as json_file:
#     data = json.load(json_file)
#     # print(data)
#     # data = str(data)
#     print(client.post_object(data))
    
