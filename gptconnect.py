from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import json
import base64
import threading

class GPTConnect():
    def __init__(self):
        with open('accounts.json') as accounts:
            self.accounts = json.loads(accounts.read())
        self.curr_username = None
    
    def load(self, scraper_path):
        for account in self.accounts:
            options = uc.ChromeOptions()
            options.add_argument("--headless=new")
            self.drive = uc.Chrome(options=options)
            self.drive.get("https://chat.openai.com/auth/login")
            self.drive.implicitly_wait(20)
            self.curr_username = account['username']
            self.login(account['username'], account['password'], account['auth_method'])
            self.remove_popups()
            self.execute_scraper(scraper_path)

    def login(self, username, password, auth_method):
        print(f'({self.curr_username}) Logging in using {auth_method} auth.')
        self.drive.find_element(
            By.XPATH, '//button[@class="btn relative btn-primary"]').click()
        
        if auth_method == 'gpt':
            self.drive.find_element(
                By.XPATH, '//input[@name="username"]').send_keys(username)
            self.drive.find_element(By.XPATH, '//button[@type="submit"]').click()
            self.drive.find_element(
                By.XPATH, '//input[@name="password"]').send_keys(base64.b64decode(password).decode('utf-8'))
            self.drive.find_element(By.CSS_SELECTOR, '._button-login-password').click()

        if auth_method == 'google':
            self.drive.find_element(
                By.XPATH, '//button[@class="c9896a921 c83665ce2 c0062c0fe"]').click()
            self.drive.find_element(
                By.XPATH, '//input[@class="whsOnd zHQkBf"]').send_keys(username)
            self.drive.find_element(
                By.XPATH, '//div[@id="identifierNext"]').click()
            self.drive.find_element(
                By.XPATH, '//input[@autocomplete="current-password"]').send_keys(base64.b64decode(password).decode('utf-8'))
            self.drive.find_element(
                By.XPATH, '//div[@id="passwordNext"]').click()


    def remove_popups(self):
        print(f'({self.curr_username}) Removing pop-ups.')
        for _ in range(3):
            self.drive.implicitly_wait(50)
            self.drive.find_element(
                        By.CSS_SELECTOR, 'button.ml-auto').click()

    def execute_scraper(self, scraper_path):
        print(f'({self.curr_username}) Executing scraper on chat-gpt.')
        with open(scraper_path, 'r') as js:
            self.drive.execute_script(js.read())
