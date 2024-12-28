import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from config import LINKEDIN_PASSWORD, LINKEDIN_USERNAME, DRIVER_PATH, DEBUG_SCREENSHOT_DIR
class Linkedin:

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
        options.add_argument("--window-size=1920,1080")  # Set a suitable window size

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
            print("--Don't remember me")
            label = form.find_element(By.CSS_SELECTOR, "label[for='rememberMeOptIn-checkbox']")
            label.click()
        submit_button = form.find_element(by=By.TAG_NAME, value="button")
        submit_button.click()
        current_url = self.driver.current_url
        if "linkedin.com/feed/" in current_url:
            print("Login successful!")
        else:
            print("Login failed.")
            raise Exception("Login Failed.")
        time.sleep(2)

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
            self.scroll_to_bottom_of_listings()
        job_containers = d.find_elements(By.CSS_SELECTOR, "div.scaffold-layout__list > div > ul > li")
        job_elements = []
        for i, job in enumerate(job_containers):
            time.sleep(1)
            try:
                job_details = self.get_job_details(job)
            except:
                print("Creating screenshot..")
                d.save_screenshot(f"{DEBUG_SCREENSHOT_DIR}debug.png")
                self.scroll_to(job)
                job_details = self.get_job_details(job, i)

            job_elements.append(job_details)
            print("Job imported")
        print("Returning job elements..")
        return job_elements
    
    def set_search_criteria(self):
        print("Setting search criteria..")
        d = self.driver
        d.get(f"{self.JOBS_RESOURCE}/?keywords={self.params["keywords"]}&location={self.params["location"]}")
        time.sleep(2)

        print("Set advanced filters..")
        advanced_filters = d.find_element(By.CSS_SELECTOR, "[aria-label='Show all filters. Clicking this button displays all available filter options.']")
        advanced_filters.click()
        time.sleep(1)
        # For now I'm going to hardcode all of my filters
        print("...")
        d.find_element(By.CSS_SELECTOR, "[for='advanced-filter-timePostedRange-r86400']").click()
        d.find_element(By.CSS_SELECTOR, "[for='advanced-filter-workplaceType-2']").click()
        d.find_element(By.CSS_SELECTOR, "[aria-label^='Apply current filters']").click()
        print("Filters applied.")

    def scroll_to_bottom_of_listings(self):
        print("Scroll to bottom..")
        d = self.driver
        job_list = d.find_element(By.CSS_SELECTOR, "div.scaffold-layout__list > div")
        last_height = d.execute_script("return arguments[0].scrollHeight", job_list)
        while True:
            d.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", job_list)
            d.execute_script("arguments[0].dispatchEvent(new Event('scroll'))", job_list)
            time.sleep(0.5)
            new_height = d.execute_script("return arguments[0].scrollHeight", job_list)
            if new_height == last_height:
                break
            last_height = new_height
        time.sleep(2)
        print("Scroll complete.")

    def get_job_details(self, job, i):
        # attribute data-job-id                                             = external_job_id
        external_job_id = job.find_element(By.CLASS_NAME, "job-card-container").get_attribute("data-job-id")
        # class     job-card-list__title--link      attribute   aria-label  = job_title
        print(f"Found job with id: {external_job_id}")
        job_card_link   = job.find_element(By.CLASS_NAME, "job-card-list__title--link")
        job_title       = job_card_link.text.split("\n")[0]
        # class     artdeco-entity-lockup__subtitle                         = company
        company         = job.find_element(By.CLASS_NAME, "artdeco-entity-lockup__subtitle").text
        # class     artdeco-entity-lockup__caption                          = location
        location        = job.find_element(By.CLASS_NAME, "artdeco-entity-lockup__caption").text
        # id        job-details                                             = description
        if i != 0:
            job_card_link.click()
        description     = self.driver.find_element(By.ID, "job-details").text

        return {
            "external_job_id"   : external_job_id,
            "job_title"         : job_title,
            "company"           : company,
            "location"          : location,
            "description"       : description,
            "source"            : "Linkedin"
        }

    def scroll_to(self, element):
        ActionChains(self.driver)\
            .move_to_element(element)\
            .pause(1)\
            .perform()
        time.sleep(1)


    def get_results(self):
        try:
            return self.begin_search()
        except Exception as e:
            self.driver.save_screenshot(f"{DEBUG_SCREENSHOT_DIR}debug-exception.png")
            return { "error": str(e) }
        finally:
            self.driver.quit()