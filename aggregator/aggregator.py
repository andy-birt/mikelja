class JobAggregator:
    def __init__(self, api_clients, scrapers):
        self.api_clients = api_clients
        self.scrapers = scrapers

    def fetch_all_jobs(self):
        aggregated_jobs = []
        for client in self.api_clients:
            jobs = client.get_results()
            aggregated_jobs.append(jobs)
        return aggregated_jobs
    
    def scrape(self):
        aggregated_jobs = []
        for scraper in self.scrapers:
            jobs = scraper.get_results()
            aggregated_jobs.append(jobs)
        return aggregated_jobs