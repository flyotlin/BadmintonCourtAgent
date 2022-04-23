from time import sleep
from .agent import Agent


class Checker(Agent):
    def __init__(self) -> None:
        super().__init__()

    def check(self):
        self.goto_spot_and_sport()

        courts = self.driver.find_elements_by_xpath('//*[@id="vue-branch-app"]/div[2]/div/ul/li')
        for i in courts:
            sleep(2)
            select_btn = i.find_element_by_xpath('//a[@class="price primary-business-color-background-hover"]')
            self.click(select_btn)

            # iterate all enabled date

            # click right btn

            # iterate all enabled date

            sleep(2)
            self.goback()
