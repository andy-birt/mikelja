import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from config import LINKEDIN_PASSWORD, LINKEDIN_USERNAME, DRIVER_PATH
class Linkedin:

    # Need a way to identify the elements on a page as these change over time.

    # 1. Simulate going to Linkedin website
    # 2. Login with burner creds
    # 3. Simulate a job search - set search filters
    # 4. Inital scrape
    #   a. Get jobs on first page and selected details.

    # This is the URL I had when searching Linkedin and wasn't restricted to seeing 3 jobs as a guest
    # https://www.linkedin.com/jobs/search?keywords=python&location=United%20States&geoId=103644278&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0

    BASE_URL = "https://www.linkedin.com"
    JOBS_URL = BASE_URL + "/jobs"
    JOBS_RESOURCE = BASE_URL + "/jobs/search"
    service = Service(DRIVER_PATH)
    
    def __init__(self, params = None):
        self.params = params
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-logging")  # Suppress unnecessary logging
        options.add_argument("--log-level=3")  # Minimize log output
        options.add_argument("--disable-blink-features=WebRTC")  # Disables WebRTC-related features

        self.driver = webdriver.Chrome(service=self.service, options=options)

    def login(self):
        url = "https://www.linkedin.com/login"
        d = self.driver
        d.get(url)
        time.sleep(2)
        form = d.find_element(by=By.CLASS_NAME, value="login__form")
        username_field = form.find_element(by=By.ID, value="username")
        password_field = form.find_element(by=By.ID, value="password")
        username_field.send_keys(LINKEDIN_USERNAME)
        password_field.send_keys(LINKEDIN_PASSWORD)
        remember_me = form.find_element(by=By.ID, value="rememberMeOptIn-checkbox")
        if remember_me.is_selected:
            print("don't remember me")
            label = form.find_element(By.CSS_SELECTOR, "label[for='rememberMeOptIn-checkbox']")
            label.click()
        submit_button = form.find_element(by=By.TAG_NAME, value="button")
        submit_button.click()
        current_url = self.driver.current_url
        if "linkedin.com/feed/" in current_url:
            print("Login successful!")
        else:
            print("Login failed.")

    def begin_search(self):
        d = self.driver
        d.get(self.BASE_URL)
        nav_tags = d.find_elements(By.TAG_NAME, "nav")
        script_tags = d.find_elements(By.TAG_NAME, "script")
        is_too_many_requests = False
        is_signin_required = False
        for script in script_tags:
            html = script.get_attribute("innerHTML").lower()
            if "http error 429" in html:
                is_too_many_requests = True
        for tag in nav_tags:
            text = tag.text.lower()
            if "sign in" in text:
                is_signin_required = True
        if is_signin_required or is_too_many_requests or "sign up" in d.title.lower():
            print("Logging in...")
            self.login()
            self.set_search_criteria()
            # d.get(self.RESOURCE)
        job_containers = d.find_elements(By.CLASS_NAME, "job-card-container")
        job_elements = []
        for i, job in enumerate(job_containers):
            # attribute data-job-id                                             = external_job_id
            external_job_id = job.get_attribute("data-job-id")
            # class     job-card-list__title--link      attribute   aria-label  = job_title
            job_card_link   = job.find_element(By.CLASS_NAME, "job-card-list__title--link")
            job_title       = job_card_link.text.split("\n")[0]
            # class     artdeco-entity-lockup__subtitle                         = company
            company         = job.find_element(By.CLASS_NAME, "artdeco-entity-lockup__subtitle").text
            # class     artdeco-entity-lockup__caption                          = location
            location        = job.find_element(By.CLASS_NAME, "artdeco-entity-lockup__caption").text
            # id        job-details                                             = description
            if i != 0:
                job_card_link.click()
            description     = d.find_element(By.ID, "job-details").text

            scraped_job = {
                "external_job_id"   : external_job_id,
                "job_title"         : job_title,
                "company"           : company,
                "location"          : location,
                "description"       : description,
                "source"            : "Linkedin"
            }

            job_elements.append(scraped_job)

        return job_elements
    
    def set_search_criteria(self):
        d = self.driver
        d.get(f"{self.JOBS_RESOURCE}/?keywords={self.params["keywords"]}&location={self.params["location"]}")
        time.sleep(2)
        # search_keyword_input  = d.find_element(By.CSS_SELECTOR, "[aria-label='Search by title, skill, or company']")
        # search_location_input = d.find_element(By.CSS_SELECTOR, "[aria-label='City, state, or zip code']")

        # Search by this keyword/location
        # search_keyword_input.send_keys(self.params["keywords"])
        # search_location_input.send_keys(self.params["location"])

        # submit_search_button = d.find_element(By.CLASS_NAME, "jobs-search-box__submit-button")
        # d.execute_script("arguments[0].click();", submit_search_button)

        # Now let's make sure we're only looking for jobs based on our other filters
        advanced_filters = d.find_element(By.CSS_SELECTOR, "[aria-label='Show all filters. Clicking this button displays all available filter options.']")
        advanced_filters.click()
        
        # For now I'm going to hardcode all of my filters
        d.find_element(By.CSS_SELECTOR, "[for='advanced-filter-timePostedRange-r86400']").click()
        d.find_element(By.CSS_SELECTOR, "[for='advanced-filter-workplaceType-2']").click()
        d.find_element(By.CSS_SELECTOR, "[aria-label^='Apply current filters']").click()

    def get_results(self):
        try:
            return self.begin_search()
        except Exception as e:
            return { "error": str(e) }
        finally:
            self.driver.quit()