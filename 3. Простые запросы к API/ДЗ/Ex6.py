import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect")
for item in response.history:
    print(item.url)