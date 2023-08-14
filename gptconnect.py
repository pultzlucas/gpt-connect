from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import json
import base64

import chromedriver_autoinstaller as chromedriver
chromedriver.install()

class GPTConnect():
    def __init__(self):
        self.accounts = self.get_accounts()
        self.curr_username = None
        self.scraper_path = None

    def get_accounts(self):
        try:
            with open('accounts.json') as accounts:
                return json.loads(accounts.read())
        except:
            print('[ERROR] Unable to find "accounts.json" file.')
            exit(1)

    def load_scraper(self, scraper_path):
        self.scraper_path = scraper_path

    def run(self):
        for account in self.accounts:
            options = uc.ChromeOptions()
            options.headless = True
            options.add_argument("--no-sandbox")
            # options.add_argument(r'--user-data-dir=c:\\Users\\NAPP\AppData\\Local\\Google\\Chrome\\User Data')
            # options.add_argument('--profile-directory=Profile 1')
            

            self.driver = uc.Chrome(options=options, driver_executable_path='./chromedriver.exe')

            self.driver.get("https://chat.openai.com/auth/login")
            self.driver.implicitly_wait(20)
            self.curr_username = account['username']
            self.login(account['username'], account['password'], account['auth_method'])
            self.remove_popups()
            self.execute_scraper(self.scraper_path)

    def login(self, username, password, auth_method):
        print(f'({self.curr_username}) Logging in using {auth_method} auth.')
        try:
            self.driver.find_element(
                By.XPATH, '//button[@class="btn relative btn-primary"]').click()
            
            if auth_method == 'gpt':
                self.driver.find_element(
                    By.XPATH, '//input[@name="username"]').send_keys(username)
                self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()
                self.driver.find_element(
                    By.XPATH, '//input[@name="password"]').send_keys(base64.b64decode(password).decode('utf-8'))
                self.driver.find_element(By.CSS_SELECTOR, '._button-login-password').click()

            if auth_method == 'google':
                self.driver.find_element(
                    By.XPATH, '//button[@class="c9896a921 c83665ce2 c0062c0fe"]').click()
                self.driver.find_element(
                    By.XPATH, '//input[@class="whsOnd zHQkBf"]').send_keys(username)
                self.driver.find_element(
                    By.XPATH, '//div[@id="identifierNext"]').click()
                self.driver.find_element(
                    By.XPATH, '//input[@autocomplete="current-password"]').send_keys(base64.b64decode(password).decode('utf-8'))
                self.driver.find_element(
                    By.XPATH, '//div[@id="passwordNext"]').click()
        except:
            print(f'({self.curr_username}) [ERROR] Error when logging in.')
            exit(1)

    def remove_popups(self):
        print(f'({self.curr_username}) Removing chat pop-ups.')
        try:
            for _ in range(3):
                self.driver.implicitly_wait(50)
                self.driver.find_element(
                            By.CSS_SELECTOR, 'button.ml-auto').click()
        except:
            print(f'({self.curr_username}) [ERROR] Error when removing chat pop-ups.')
            exit(1)

    def execute_scraper(self, scraper_path, account_id):
        print(f'({self.curr_username}) Executing scraper on chat-gpt.')
        try:
            with open(scraper_path, 'r', encoding='utf-8') as js:
                script = js.read().replace('@@account_id@@')
                self.driver.execute_script(script)
        except:
            print(f'({self.curr_username}) [ERROR] Unable to find scraper file "{scraper_path}".')
            exit(1)
