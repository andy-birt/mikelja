from config import PROXY_FILE
import random

class Proxee:

    def __init__(self):
        self.proxies = self.populate_proxies()
        self.proxy_dicts = [{ proxy: {"http": f"http://{proxy}", "https": f"https://{proxy}"}} for proxy in self.proxies]

    def populate_proxies(self):
        proxies = []
        with open(PROXY_FILE, "r") as file:
            proxies = [line.strip() for line in file]
        return proxies
    
    def set_proxy(self):
        self.proxy = random.choice(self.proxies)

    def get_proxy_dict(self):
        for proxy in self.proxy_dicts:
            for k in proxy.keys():
                if k == self.proxy:
                    return proxy
        return None