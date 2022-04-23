from selenium.common.exceptions import NoSuchElementException
from time import sleep
from .agent import Agent


class Checker(Agent):
    def __init__(self) -> None:
        super().__init__()
        self.court_info_records = []

    def check(self):
        self.goto_spot_and_sport()

        # we should keep record of (court#, date, time), so later applier can apply for this directly
        self.court_info_records = []
        record = {
            'court_id': '',
            'date_id': '',
            'date': '',
            'time': ''
        }

        # after driver.back(), previous fetched elements would get stale
        courts = self.driver.find_elements_by_xpath('//*[@id="vue-branch-app"]/div[2]/div/ul/li')
        courts_num = len(courts)
        for court_id in range(1, courts_num + 1):
            court = self.driver.find_element_by_xpath(f'//*[@id="vue-branch-app"]/div[2]/div/ul/li[{court_id}]')
            # if you add // in front of a[@class], that's why we always get the first one
            select_btn = court.find_element_by_xpath('.//a[@class="price primary-business-color-background-hover"]')
            self.click(select_btn)

            idx = 1
            while True:
                try:
                    date = self.driver.find_element_by_xpath(f'//*[@id="day-selector-v2"]/div/div/div[{ idx }]')
                except NoSuchElementException:
                    print('There\'s no more date for this court')
                    break
                self.click(date)
                sleep(0.5)
                date_text = date.text

                try:
                    times = self.driver.find_elements_by_class_name('stime')
                    print(times)
                    for time in times:
                        time_text = time.text
                        record['court_id'] = court_id
                        record['date_id'] = idx
                        record['date'] = date_text
                        record['time'] = time_text
                        self.court_info_records.append(record.copy())
                except NoSuchElementException:
                    print('There\'s no li inside ul')

                idx += 1
                sleep(0.5)

            self.goback()
            sleep(1)
