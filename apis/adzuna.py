import requests
from config import ADZUNA_APP_KEY, ADZUNA_APP_ID

class Adzuna:

    BASE_URL = "https://api.adzuna.com/v1/api/jobs/us/search/"

    def __init__(self, page = 1, params = None, app_id = None, app_key = None):
        params["app_id"] = app_id or ADZUNA_APP_ID
        params["app_key"] = app_key or ADZUNA_APP_KEY
        self.page = str(page)
        self.params = params
    
    def get_results(self):
        url = self.BASE_URL + self.page
        results = requests.get(url, params=self.params)
        try:
            return results.json()
        except:
            return results.text