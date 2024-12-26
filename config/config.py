import os
from dotenv import load_dotenv

load_dotenv()

# Adzuna
ADZUNA_APP_ID   = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY  = os.getenv("ADZUNA_APP_KEY")

# Jooble
JOOBLE_API_KEY  = os.getenv("JOOBLE_API_KEY")

# Linkedin - Doesn't use an API, use with caution
LINKEDIN_USERNAME = os.getenv("LINKEDIN_USERNAME")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

# Usajobs
USAJOBS_API_KEY = os.getenv("USAJOBS_API_KEY")
USAJOBS_EMAIL   = os.getenv("USAJOBS_EMAIL")

# Webdriver
DRIVER_PATH     = os.getenv("DRIVER_PATH")