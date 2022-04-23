from selenium.common.exceptions import NoSuchElementException
from time import sleep
from .agent import Agent


class Applier(Agent):
    def __init__(self) -> None:
        super().__init__()

    def apply(self, court_id: str, date_id: str, _time: str):
        self.goto_spot_and_sport()

        # go to court_id
        court = self.driver.find_element_by_xpath(f'//*[@id="vue-branch-app"]/div[2]/div/ul/li[{court_id}]')
        select_btn = court.find_element_by_xpath('.//a[@class="price primary-business-color-background-hover"]')
        self.click(select_btn)

        # go to date_id
        date = self.driver.find_element_by_xpath(f'//*[@id="day-selector-v2"]/div/div/div[{ date_id }]')
        self.click(date)
        sleep(0.5)

        # select btn in this time
        try:
            times = self.driver.find_elements_by_class_name('stime')
            print(times)
            # assume arguments passed is correct (but we should do error handling here in the future)
            for time in times:
                time_text = time.text
                if time_text != _time:
                    continue

                # find select btn
                time.find_element_by_tag_name
                select_time_div = time.find_element_by_xpath('..')
                select_btn = select_time_div.find_element_by_tag_name('a')
                self.click(select_btn)
                sleep(0.5)

                # apply / reserve
                apply_btn = self.driver.find_element_by_xpath('//*[@id="confirm_booking"]/div[2]')
                self.click(apply_btn)

        except NoSuchElementException:
            print('There\'s no li inside ul')
