import re
import sys
import json
import requests

from typing import Literal, TypedDict

import mechanicalsoup

class BatmintonReserveAgent():
    BaseCookie = TypedDict('Cookie', {'PHPSESSID': str, 'XSRF-TOKEN': str, '17fit_system_session': str})
    def __init__(self, cookie: BaseCookie) -> None:
        self.browser = mechanicalsoup.StatefulBrowser(
            raise_on_404=True,
        )

        self.browser.set_cookiejar(requests.cookies.cookiejar_from_dict(cookie))


    GET_COURT_URL = 'https://17fit.com/service-flow-sp'
    GET_COURT_BODY = {
        'currency': 'NT$',
        'studio_id': '1090',
        'branch_id': '1275',
        'selected_services': '28055',
        'selected_services_namelist': '羽球館場地預約',
        'selected_services_timetotal': '1+小時0+分鐘',
        'selected_services_pricetotal': '400',
        'service_url': 'https://17fit.com/NCUsportscenter/01?tab=appointments',
    }
    GET_COURT_PATTERNS = r'\[\{.*"member_id".*:.*,.*"member_name".*:.*\}\]'
    Court = TypedDict('Court', {'member_id': int, 'member_name': str, 'role_relationships_id': int, 'level_price': int})
    def _get_courts(self) -> list[Court]:
        html = self.browser.post(self.GET_COURT_URL, self.GET_COURT_BODY).text
        courts_json = re.compile(self.GET_COURT_PATTERNS).findall(html)
        assert len(courts_json) == 1, 'courts: pattern did not matched'
        return json.loads(courts_json[0])


    SET_CURRENT_COURT_URL = 'https://17fit.com/service-flow-dt'
    def _set_current_court(self, court: Court) -> None:
        self.browser.post(self.SET_CURRENT_COURT_URL, court)


    GET_PROVIDER_DATETIME_URL = 'https://17fit.com/getServiceProviderDateTimeApi'
    Datetime = TypedDict('Datetime', {'available_role_relationship_ids': list[int], 'date': str, 'datetime': str, 'time': str})
    def _get_provider_datetimes(self) -> list[Datetime]:
        datetimes_json = self.browser.post(self.GET_PROVIDER_DATETIME_URL).json()
        return datetimes_json


    SET_CURRENT_DATETIME_URL = 'https://17fit.com/service-flow-confirm'
    SET_CURRENT_DATETIME_PATTERNS = r'\[\{.*"id".*:.*,.*"studio_id".*:.*\}\]'
    def _set_current_datetime(self, time: Datetime) -> str:
        html = self.browser.post(self.SET_CURRENT_DATETIME_URL, {
            'is_cash': 0,
            'selected_time': time['time'],
            'selected_day': time['date'],
        }).text
        datetimes_json = re.compile(self.SET_CURRENT_DATETIME_PATTERNS).findall(html)
        assert len(datetimes_json) == 1, 'datetimes: pattern did not matched'
        return json.loads(datetimes_json[0])[0]['id']


    SET_RESERVE_URL = 'https://17fit.com/service-flow-make-appointment'
    def _reserve(self, id) -> None:
        self.browser.post(self.SET_RESERVE_URL, {
            'client_booking_note': 'ya',
            'pay_method': 'cash',
            'contract_selected': '{' + f'"{id}": 0' + '}',
            'studio_payment_method_id': 1,
        })


    COURTS=Literal['近講臺右', '近講臺中', '近講臺左', '近門口右', '近門口中', '近門口左']
    def go(self, time: str, courts: tuple[COURTS], maximun_at_the_same_time: int):
        all_courts = self._get_courts()
        courts = list(filter(lambda x: x['member_name'].endswith(courts), all_courts))
        result = []

        count_of_the_same_time = 0
        for court in courts:
            self._set_current_court(court)
            all_datetimes = self._get_provider_datetimes()

            if len(list(filter(lambda x: x['datatime'] == time, all_datetimes))) > 0:
                self._set_current_datetime(time)
                self._reserve()

                count_of_the_same_time += 1
                result.append({'success': True, 'message': f'success: reserve court {court} at {time}'})
            else:
                result.append({'success': False, 'message': f'fail: no court {court} at {time}'})

            if count_of_the_same_time >= maximun_at_the_same_time:
                break

        return {}



if __name__ == '__main__':
    try:
        aya = BatmintonReserveAgent({'PHPSESSID': 'a','XSRF-TOKEN': 'b', '17fit_system_session': 'c'})
        results = aya.go(
            time="2022-04-29 18:00:00",
            courts=('近講臺左', '近講臺右'),
            maximun_at_the_same_time=2
        )
    except Exception as e:
        # TODO: send message to telegram if encountered unexpected error
        print(sys.exc_info())