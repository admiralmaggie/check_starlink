import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
import requests
import sys
import time


class Robotics:
    delay = 10000
    email = None
    password = None
    location = None
    mail_key = '[your mailgun API key]'
    mail_sandbox = '[your mailgun sandbox URL]'
    mail_recipient = 'recipient <email@email.eml>'
    mail_from = 'sender <email@email.eml>'
    mail_subject = 'Starlink Order Status'

    status = None

    def __init__(self, email, password, location):
        self.email = email
        self.password = password
        self.location = location

    def go(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--disable-blink-features=AutomationControlled')
        driver = webdriver.Chrome(options=options)
        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

        driver = webdriver.Chrome(options=options)
        driver.get('https://www.starlink.com/account/home')

        WebDriverWait(driver, self.delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mat-input-0"]')))
        driver.implicitly_wait(self.delay)
        driver.find_element(by=By.NAME, value='email').send_keys(self.email)
        time.sleep(1)
        driver.find_element(by=By.NAME, value='password').send_keys(self.password)
        time.sleep(1)
        driver.find_element(by=By.XPATH, value='/html/body/app-root/div/public-header-navigation/div/mat-drawer-container/mat-drawer-content/div/app-login/app-center-box/div/div/form/div[4]/button').click()
        time.sleep(1)

        xpath_order_deposit = "/html/body/app-root/starlink-nav-layout/div/mat-sidenav-container/"\
                              "mat-sidenav-content/div/main/app-account-home/div/div[1]/"\
                              "app-info-pane-prepay/section/app-deposit-section/article/div[1]"
        WebDriverWait(driver, self.delay).until(EC.presence_of_element_located((By.XPATH, xpath_order_deposit)))

        xpath_status = "/html/body/app-root/starlink-nav-layout/div/mat-sidenav-container/"\
                       "mat-sidenav-content/div/main/app-account-home/div/div[2]/"\
                       "app-notice-section/article/span"
        self.status = driver.find_element(by=By.XPATH, value=xpath_status).text

        print('Status:', self.status)

        self.send_mail()
        return

    def send_mail(self):
        request_url = 'https://api.mailgun.net/v3/{0}/messages'.format(self.mail_sandbox)

        html_text = "<h3>Starlink Order Status, Checked on {date}</h3><br/>" \
                    "Status: <b>{status}</b><br/>Location: <b>{location}</b>".format\
                                (date=datetime.date.strftime(datetime.date.today(), "%m/%d/%Y"),
                                 status=self.status,
                                 location=self.location)
        requests.post(request_url, auth=('api', self.mail_key), data={
            'from': self.mail_from,
            'to': self.mail_recipient,
            'subject': self.mail_subject,
            'html': html_text})


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print('Please provide required parameters (email, password, location)!')
        exit(1)
    robot = Robotics(email=sys.argv[1], password=sys.argv[2], location=sys.argv[3])
    robot.go()
