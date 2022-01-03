import requests

from Environment import *

# Get запрос - params Post запрс - data
response = requests.post(check_get_500_url)
print(response.status_code)
print(response.text)
response2 = requests.post(check_get_301_url, allow_redirects=True)
first_response = response2.history[0]
second_response = response2
print(first_response.url)
print(second_response.url)
