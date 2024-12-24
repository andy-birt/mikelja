import requests

class Remotive:

    BASE_URL = "https://remotive.com/api/remote-jobs"
    
    def __init__(self, params = None):
        self.params = params
    
    def get_results(self):
        url = self.BASE_URL
        results = requests.get(url, params=self.params)
        try:
            return results.json()
        except:
            return results.text