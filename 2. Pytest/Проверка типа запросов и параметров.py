import requests

from LearnQA_PythonAPI.Environment import check_type_url
# Get запрос - params Post запрс - data
response = requests.post(check_type_url, data={"param1": "value1"})
print(response.text)