import configparser

from time import sleep
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement


class Agent(object):
    url_for_17fit = 'https://17fit.com/'
    driver_path = './chromedriver'

    def __init__(self) -> None:
        self.driver = webdriver.Chrome(self.driver_path)

        config = configparser.ConfigParser()
        config.read('./.env')
        self.phone_number = config['17-fit']['phone_number']
        self.pwd = config['17-fit']['pwd']

    def goto(self, url: str):
        self.driver.get(url)

    def goback(self):
        self.driver.back()

    def fill_in(self, element: WebElement, text: str):
        element.send_keys(text)

    def clear(self, element: WebElement):
        element.clear()

    def click(self, element: WebElement):
        element.click()

    def login(self):
        self.goto(self.url_for_17fit)

        login_btn = self.driver.find_element_by_class_name('login')
        self.click(login_btn)

        phone = self.driver.find_element_by_xpath("//input[@name='phone']")
        self.fill_in(phone, self.phone_number)

        pwd = self.driver.find_element_by_xpath("//input[@name='password']")
        self.fill_in(pwd, self.pwd)

        login_btn = self.driver.find_element_by_xpath("//input[@value='登入']")
        self.click(login_btn)

    def logout(self):
        self.goto(self.url_for_17fit + 'logout')

    def goto_spot_and_sport(
        self,
        spot: str = 'NCUsportscenter/01?tab=appointment',
        sport: str = "//*[@id=\"service_accordion_list2\"]/div/div/div/div[2]/div[2]/span[2]/a"
    ):
        sleep(5)    # why we need to wait for like 5 sec ?
        self.goto(self.url_for_17fit + spot)

        apply_btn = self.driver.find_element_by_xpath(sport)
        self.click(apply_btn)

    def bye(self):
        self.driver.close()
