class JobAggregator:
    def __init__(self, api_clients):
        self.api_clients = api_clients

    def fetch_all_jobs(self):
        aggregated_jobs = []
        for client in self.api_clients:
            jobs = client.get_results()
            aggregated_jobs.append(jobs)
        return aggregated_jobs