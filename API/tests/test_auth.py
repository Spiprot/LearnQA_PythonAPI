import requests
import pytest
from LearnQA_PythonAPI.API.lib.base_case import BaseCase
from LearnQA_PythonAPI.API.lib.assertions import Assertions


class TestUserAuth(BaseCase):
    exclude_params = [
        "no_cookie",
        "no_token"
    ]
    url_login = "https://playground.learnqa.ru/api/user/login"
    url_auth = "https://playground.learnqa.ru/api/user/auth"

    def setup(self):
        data = {
            "email": 'vinkotov@example.com',
            "password": "1234"
        }
        response1 = requests.post(self.url_login, data=data)
        self.check_response_code(response1)
        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")

    def test_auth_user(self):
        response2 = requests.get(
            url=TestUserAuth.url_auth,
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )
        Assertions.assert_json_value_by_name(
            response=response2,
            name="user_id",
            expected_value=self.user_id_from_auth_method,
            error_message="User ID from auth method is not equal to user id from check method"
        )

    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):
        if condition == "no_cookie":
            response2 = requests.get(
                url=self.url_auth,
                headers={"x-csrf-token": self.token}
            )
        else:
            response2 = requests.get(
                url=self.url_auth,
                cookies={"auth_sid": self.auth_sid}
            )
        Assertions.assert_json_value_by_name(
            response=response2,
            name="user_id",
            expected_value=0,
            error_message='f"User is authorized with condition {condition}'
        )
