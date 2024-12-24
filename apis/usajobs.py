import requests
from config import USAJOBS_EMAIL, USAJOBS_API_KEY

class Usajobs:

    BASE_URL = "https://data.usajobs.gov/api/search"

    def __init__(self, headers = None, params = None):
        if headers is None:
            headers = {
                "Authorization-Key": USAJOBS_API_KEY,
                "User-Agent": USAJOBS_EMAIL
            }
        self.params = params
        self.headers = headers
    
    def get_results(self):
        url = self.BASE_URL
        results = requests.get(url, params=self.params, headers={"Authorization-Key": self.headers["Authorization-Key"], "User-Agent": self.headers["User-Agent"]})
        try:
            return results.json()
        except:
            return results.text