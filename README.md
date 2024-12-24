## Quick Start

Once you clone this, create a virtual environment
```bash
> python -m venv venv
```

Activate the Virtual Environment

Windows:
```bash
> .\venv\Scripts\activate
```
Mac/Linux:
```bash
> source venv/bin/activate
```

Install Dependencies
```bash
> pip install -r requirements.txt
```

Get started quickly by testing with Remotive since you don't need a key
```python
from apis import Remotive

remotive_params = {
    "search": "c#"
}

test_search = Remotive(params=remotive_params)

r = test_search.get_results()

# please work...
print(r)
```

Create a `.env` file to keep your credentials
```env
# If you're using any source control don't forget to ignore this file!
ADZUNA_APP_ID=[APP_ID]
ADZUNA_APP_KEY=[APP_KEY]
```

```python
# Create a new search for Adzuna
from apis import Adzuna

# Refer to Adzuna API docs for full list of parameters
params = {
    "results_per_page": 25,
    "what_and": "software engineer c# remote",
    "max_days_old": 5,
    "salary_min": 80000,
    "full_time": "1"
}

new_search = Adzuna(page=1, params=params)

r = new_search.get_results()

# Display the JSON results
print(r)
```
## Aggregator Example

```py
from apis import Adzuna, Remotive, Usajobs
from aggregator import JobAggregator

adzuna_params = {
    "results_per_page": 25,
    "what_and": "software engineer c# remote",
    "max_days_old": 5,
    "salary_min": 80000,
    "full_time": "1"
}

remotive_params = {
    "search": "c#"
}

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

# Look at dem jobbies!
print(data)
```