# Untested - API key has 500 request limit - yikes...
import requests
from config import JOOBLE_API_KEY
class Jooble:
    # It looks like with Jooble you have to make POST requests to get jobs
    ## From Jooble Docs
    # import http.client

    # host = 'jooble.org'
    # key = '<YOUR_API_KEY>'

    # connection = http.client.HTTPConnection(host)
    # #request headers
    # headers = {"Content-type": "application/json"}
    # #json query
    # body = '{ "keywords": "it", "location": "Bern"}'
    # connection.request('POST','/api/' + key, body, headers)
    # response = connection.getresponse()
    # print(response.status, response.reason)
    # print(response.read())

    BASE_URL = "https://jooble.org/api/"

    def __init__(self, page = 1, params = None, api_key = None):
        params["api_key"] = api_key or JOOBLE_API_KEY
        self.page = str(page)
        self.params = params
    
    def get_results(self):
        url = self.BASE_URL + self.page
        results = requests.get(url, params=self.params)
        try:
            return results.json()
        except:
            return results.text