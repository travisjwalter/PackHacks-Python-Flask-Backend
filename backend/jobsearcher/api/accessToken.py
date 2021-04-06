import requests
import json

## This file provides the API functionality to get the access_token for the Indeed API.
## @author Travis Walter - 3/16/2021

## This is an example HTTP POST reqest to an outside API. We don't use this in the project
## but I wanted to talk through it if people were interested.
def getAccessToken(clientID, clientSecret): 
    url = "https://apis.indeed.com/oauth/v2/tokens?client_id={clientID}&client_secret={clientSecret}&grant_type=client_credentials"

    payload={}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'Cookie': 'CTK=1f0trs58bu2du801; SURF=Kzwvk0Uv34Of5LqSYsJ5nqf822Nca715'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    res = json.loads(response.text)
    return res["access_token"]