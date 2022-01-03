# Сегодня задача должна быть попроще. У нас есть вот такой URL:
# https://playground.learnqa.ru/ajax/api/compare_query_type Запрашивать его можно четырьмя разными HTTP-методами:
# POST, GET, PUT, DELETE
#
# При этом в запросе должен быть параметр method. Он должен содержать указание метода, с помощью которого вы делаете
# запрос. Например, если вы делаете GET-запрос, параметр method должен равняться строке ‘GET’. Если POST-запросом -
# то параметр method должен равняться ‘POST’. И так далее.
#
# Надо написать скрипт, который делает следующее:
#
# 1. Делает http-запрос любого типа без параметра method, описать что будет выводиться в этом случае.
# 2. Делает http-запрос не из списка. Например, HEAD. Описать что будет выводиться в этом случае.
# 3. Делает запрос с правильным значением method. Описать что будет выводиться в этом случае.
# 4. С помощью цикла проверяет все возможные сочетания реальных типов запроса и значений параметра method.
# Например с GET-запросом передает значения параметра method равное ‘GET’, затем ‘POST’, ‘PUT’, ‘DELETE’ и так далее.
# И так для всех типов запроса. Найти такое сочетание, когда реальный тип запроса не совпадает со значением параметра,
# но сервер отвечает так, словно все ок. Или же наоборот, когда типы совпадают, но сервер считает, что это не так.
#
# Не забывайте, что для GET-запроса данные надо передавать через params=
# А для всех остальных через data=
#
# Итогом должна быть ссылка на коммит со скриптом и ответы на все 4 вопроса.

import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"
# п.1
response = requests.get(url)
print(response.text)
print('-----------')

# п.2
response = requests.head(url)
print(response.status_code)
print('-----------')

# п.3
response = requests.get(url, params={'method': 'POST'})
print(response.text)
print('-----------')

# п.4
# ‘GET’, затем ‘POST’, ‘PUT’, ‘DELETE’
# С помощью цикла проверяет все возможные сочетания реальных типов запроса и значений параметра method.
print('Пункт 4')
list_params = ("GET", "POST", "PUT", "DELETE",)


def check_method_with_params(method, param):
    if method == param:
        if response.text != '{"success":"!"}':
            print('Должен был быть успех')
    if method != param:
        if response.text == '{"success":"!"}':
            print('Должна была быть ошибка')


def send_request(method, param):
    global response
    if method == 'GET':
        response = requests.get(url, params={"method": param})
    elif method == 'POST':
        response = requests.post(url, data={"method": param})
    elif method == 'PUT':
        response = requests.put(url, data={"method": param})
    elif method == 'DELETE':
        response = requests.delete(url, data={"method": param})
    else:
        print('Wrong method')
    print(f'''Method = {method}, params = {param}''')
    print(response.text)
    check_method_with_params(method, param)
    print('----------')
    return response.text


for method in list_params:
    for param in list_params:
        send_request(method=method, param=param)

