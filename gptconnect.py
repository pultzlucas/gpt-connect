from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

class GPTConnect():
    def __init__(self):
        options = uc.ChromeOptions()
        # options.headless=True
        # options.add_argument('--headless')
        # chrome = uc.Chrome(options=options)
        self.drive = uc.Chrome()
    
    def load(self):
        self.drive.get("https://chat.openai.com/auth/login")
        self.drive.implicitly_wait(20)
        self.login()
        self.remove_popups()

    def login(self):
        self.drive.find_element(
            By.XPATH, '//button[@class="btn relative btn-primary"]').click()
        self.drive.find_element(
            By.XPATH, '//input[@name="username"]').send_keys('leandro.augusto.alves@outlook.com.br')
        self.drive.find_element(By.XPATH, '//button[@type="submit"]').click()
        self.drive.find_element(
            By.XPATH, '//input[@name="password"]').send_keys('Zv15936jp!')
        self.drive.find_element(By.CSS_SELECTOR, '._button-login-password').click()
        self.drive.implicitly_wait(20)

    def remove_popups(self):
        for _ in range(3):
            self.drive.implicitly_wait(50)
            self.drive.find_element(
                        By.CSS_SELECTOR, 'button.ml-auto').click()

    def execute_scraper(self, scraper_path):
        with open(scraper_path, 'r') as js:
            self.drive.execute_script(js.read())
