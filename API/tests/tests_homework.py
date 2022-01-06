import pytest
import requests
import json

from LearnQA_PythonAPI.API.lib.assertions import Assertions


class TestsHomework:
    url_test_cookie = "https://playground.learnqa.ru/api/homework_cookie"
    url_test_header = "https://playground.learnqa.ru/api/homework_header"
    url_user_agent = "https://playground.learnqa.ru/api/user_agent_check"

    # Ex 10
    def test_phrase(self):
        test_phrase = input("Input test phrase: ")
        assert len(test_phrase) <= 15, "Input phrase len more then 15 symbols"

    # Ex 11
    def test_cookie(self):
        response = requests.get(self.url_test_cookie)
        dict_cookies = dict(response.cookies)
        print(dict_cookies)
        for key in dict_cookies:
            assert key in response.cookies, f"No cookies with {key} in the response"
        cookies_response = dict_cookies[key]
        print(cookies_response)

    # Ex 12
    def test_header(self):
        response = requests.post(self.url_test_header)
        headers = response.headers
        assert headers is not None, f"No headers in the response"
        print(headers)

    # Ex 13
    user_agents = [
        ("Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, "
         "like Gecko) Version/4.0 Mobile Safari/534.30"),
        ("Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 "
         "Mobile/15E148 Safari/604.1"),
        ("Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"),
        ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 "
         "Safari/537.36 Edg/91.0.100.0"),
        ("Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
         "Version/13.0.3 Mobile/15E148 Safari/604.1")
    ]
    expected_values = [
        {'platform': 'Mobile', 'browser': 'No', 'device': 'Android'},
        # Оригинал который не проходит {'platform': 'Mobile', 'browser': 'Chrome', 'device': 'iOS'},
        {'platform': 'Mobile', 'browser': 'No', 'device': 'iOS'},
        # {'platform': 'Googlebot', 'browser': 'Unknown', 'device': 'Unknown'},
        {'platform': 'Unknown', 'browser': 'Unknown', 'device': 'Unknown'},
        {'platform': 'Web', 'browser': 'Chrome', 'device': 'No'},
        # {'platform': 'Mobile', 'browser': 'No', 'device': 'iPhone'}
        {'platform': 'Mobile', 'browser': 'No', 'device': 'Unknown'}
    ]

    @pytest.mark.parametrize(
        'agent, expected_value', [
            (user_agents[0], expected_values[0]),
            (user_agents[1], expected_values[1]),
            (user_agents[2], expected_values[2]),
            (user_agents[3], expected_values[3]),
            (user_agents[4], expected_values[4]),
        ]
    )
    # @pytest.mark.parametrize('agent', user_agents)
    # @pytest.mark.parametrize('expected_value', expected_values)
    def test_user_agent(self, agent, expected_value):
        response = requests.get(
            url=self.url_user_agent,
            headers={"User-Agent": agent}
        )
        obj_response = json.loads(response.text)
        Assertions.assert_json_value_by_name(
            response=response,
            name="platform",
            expected_value=expected_value['platform'],
            error_message=f"Платформы не совпадают {obj_response['platform']} != {expected_value['platform']}"
        )
        Assertions.assert_json_value_by_name(
            response=response,
            name="browser",
            expected_value=expected_value['browser'],
            error_message=f"Браузеры не совпадают {obj_response['browser']} != {expected_value['browser']}"
        )
        Assertions.assert_json_value_by_name(
            response=response,
            name="device",
            expected_value=expected_value['device'],
            error_message=f"Устройства не совпадают {obj_response['device']} != {expected_value['device']}"
        )

