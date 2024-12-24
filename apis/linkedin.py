# Hold off on this
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from config import LINKEDIN_PASSWORD, LINKEDIN_USERNAME
class Linkedin:

    BASE_URL = "https://www.linkedin.com/jobs"
    service = Service("C:/chromedriver/chromedriver-win32/chromedriver.exe")
    
    def __init__(self, driver, params = 'site:linkedin.com/jobs "Software Engineer" location: "Remote"'):
        self.driver = driver
        self.params = params
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
    
    def get_results(self):
        url = self.BASE_URL
        # results = requests.get(url, params=self.params, headers=self.headers)
        # soup = BeautifulSoup(results.text, "html.parser")
        # return soup
        # try:
        #     return results.json()
        # except:
        #     return results.text

    def login(self):
        self.driver.get(self.reqString)
        form = self.driver.find_element(by=By.CLASS_NAME, value="login__form")
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

    def search(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-logging")  # Suppress unnecessary logging
        options.add_argument("--log-level=3")  # Minimize log output
        options.add_argument("--disable-blink-features=WebRTC")  # Disables WebRTC-related features


        d = webdriver.Chrome(service=self.service, options=options)
        d.get(self.reqString)
        # print(d.page_source)
        nav_tags = d.find_elements(By.TAG_NAME, "nav")
        script_tags = d.find_elements(By.TAG_NAME, "script")
        is_too_many_requests = False
        is_signin_required = False
        # print(d.page_source)
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
            login = login(d, "www.linkedin.com/login")
            login.exec()
            d.get(self.reqString + self.li)
        job_list = d.find_elements(By.CLASS_NAME, "job-card-container")
        # print(job_list)
        # print(is_too_many_requests)
        for job in job_list:
            print(job.get_attribute("outerHTML"))
        d.quit()