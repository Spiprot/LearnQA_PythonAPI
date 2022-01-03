import json

import requests

from LearnQA_PythonAPI.Environment import check_show_all_headers

headers = {"some_header": "123"}

response = requests.post(check_show_all_headers, headers = headers)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
print('--------------')
print(response.headers)