########## This section I added to run this file in debug in VS Code ##########
import sys
import os
# Add the project root to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
###############################################################################

from apis import Adzuna, Remotive, Usajobs
from aggregator import JobAggregator

# Example of Adzuna API parameters
# https://developer.adzuna.com/activedocs

adzuna_params = {
    "results_per_page": 25,
    "what_and": "software engineer c# remote",
    "max_days_old": 5,
    "salary_min": 80000,
    "full_time": "1"
}

# Example of Remotive API parameters
# https://github.com/remotive-com/remote-jobs-api?tab=readme-ov-file#remote-jobs-api

remotive_params = {
    "search": "c#"
}

# Example of Usajobs API parameters
# Refine as needed for better results
# https://developer.usajobs.gov/api-reference/get-api-search

usajobs_params = {
    "Keyword": "software+engineer",
    "remoteorteleworkonly": "true",
    "whomayapply": "public",
    "dateposted": "5"
}

clients = [
    Adzuna(params=adzuna_params),
    Remotive(params=remotive_params),
    Usajobs(params=usajobs_params)
]

agg = JobAggregator(clients)

data = agg.fetch_all_jobs()

print(data)