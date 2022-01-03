import requests

from Environment import get_cookie, check_auth_cookie

payload = {"login": "secret_login", "password": "secret_pass"}

response1 = requests.post(get_cookie, data=payload)
print(response1.text)
print(response1.status_code)
print(dict(response1.cookies))
print(response1.headers)
cookie_value = response1.cookies.get('auth_cookie')
cookies = {}
if cookie_value is not None:
    cookies.update({'auth_cookie': cookie_value})

response2 = requests.post(check_auth_cookie, cookies=cookies)
print(response2.text)