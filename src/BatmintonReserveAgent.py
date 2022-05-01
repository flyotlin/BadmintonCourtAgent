import json
import mechanicalsoup
import re
import requests

from typing import Literal, TypedDict, List, Tuple


class BatmintonReserveAgent():
    BaseCookie = TypedDict('Cookie', {'PHPSESSID': str, 'XSRF-TOKEN': str, '17fit_system_session': str})
    Court = TypedDict('Court', {'member_id': int, 'member_name': str, 'role_relationships_id': int, 'level_price': int})
    Datetime = TypedDict('Datetime', {'available_role_relationship_ids': List[int], 'date': str, 'datetime': str, 'time': str})
    CourtAndDatetime = TypedDict('CourtAndDatetime', {'court': Court, 'datetime': Datetime})

    COURTS = Literal['近講臺右', '近講臺中', '近講臺左', '近門口右', '近門口中', '近門口左']

    def __init__(self, cookie: BaseCookie) -> None:
        self.browser = mechanicalsoup.StatefulBrowser(
            raise_on_404=True,
        )

        self.browser.set_cookiejar(requests.cookies.cookiejar_from_dict(cookie))

    def _get_courts(self) -> List[Court]:
        GET_COURT_PATTERNS = r'\[\{.*"member_id".*:.*,.*"member_name".*:.*\}\]'
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

        html = self.browser.post(GET_COURT_URL, GET_COURT_BODY).text
        courts_json = re.compile(GET_COURT_PATTERNS).findall(html)
        assert len(courts_json) == 1, 'courts: pattern did not matched'
        return json.loads(courts_json[0])

    def _set_current_court(self, court: Court) -> None:
        """前往羽球館的某一個場地，目的是在 session 中設定場地資訊

        Args:
            court (Court): _description_
        """
        SET_CURRENT_COURT_URL = 'https://17fit.com/service-flow-dt'

        self.browser.post(SET_CURRENT_COURT_URL, court)

    def _get_provider_datetimes(self) -> List[Datetime]:
        """取得該場地目前所有日期

        Returns:
            List[Datetime]: _description_
        """
        GET_PROVIDER_DATETIME_URL = 'https://17fit.com/getServiceProviderDateTimeApi'

        datetimes_json = self.browser.post(GET_PROVIDER_DATETIME_URL).json()
        return datetimes_json

    def _set_current_datetime(self, time: Datetime) -> str:
        SET_CURRENT_DATETIME_URL = 'https://17fit.com/service-flow-confirm'
        SET_CURRENT_DATETIME_PATTERNS = r'\[\{.*"id".*:.*,.*"studio_id".*:.*\}\]'

        html = self.browser.post(SET_CURRENT_DATETIME_URL, {
            'is_cash': 0,
            'selected_time': time['time'],
            'selected_day': time['date'],
        }).text
        datetimes_json = re.compile(SET_CURRENT_DATETIME_PATTERNS).findall(html)
        assert len(datetimes_json) == 1, 'datetimes: pattern did not matched'
        return json.loads(datetimes_json[0])[0]['id']

    def _reserve(self, id) -> None:
        SET_RESERVE_URL = 'https://17fit.com/service-flow-make-appointment'

        self.browser.post(SET_RESERVE_URL, {
            'client_booking_note': 'ya',
            'pay_method': 'cash',
            'contract_selected': '{' + f'"{id}": 0' + '}',
            'studio_payment_method_id': 1,
        })

    # TODO: the spec of batch reserve need to discuss
    def _batch_go(self, court_and_datetimes: List[CourtAndDatetime], maximun_at_the_same_time: int) -> None:
        count_of_the_same_time = {x['datetime']['datetime']: 0 for x in court_and_datetimes}
        for court_and_datetime in court_and_datetimes:
            if count_of_the_same_time[court_and_datetime['datetime']['datetime']] < maximun_at_the_same_time:
                self.go(court_and_datetime)

                count_of_the_same_time[court_and_datetime['datetime']['datetime']] += 1

    def check(self, time: str, courts: Tuple[COURTS]) -> List[CourtAndDatetime]:
        all_courts = self._get_courts()
        matched_courts = [x for x in all_courts if x['member_name'].endswith(courts)]
        result: list[self.CourtAndDatetime] = []

        for court in matched_courts:
            self._set_current_court(court)
            all_datetimes = self._get_provider_datetimes()
            if any([x for x in all_datetimes if x['datatime'] == time]):
                result.append({**court, **time})

        return result

    def go(self, court_and_datetime: CourtAndDatetime) -> None:
        """預約 courts, time 的場地

        Args:
            time (str): "2022-04-29 18:00:00" 要預約的時間
            courts (Tuple[COURTS]): 哪些場地 (參考 COURTS)
            maximun_at_the_same_time (int): 同時預約的最多場地

        Returns:
            _type_: _description_
        """
        self._set_current_court(court_and_datetime['court'])
        self._set_current_datetime(court_and_datetime['datetime']['datetime'])
        self._reserve()
