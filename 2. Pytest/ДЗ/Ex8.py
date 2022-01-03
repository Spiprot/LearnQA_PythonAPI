# Ex8: Токены
#
# Иногда API-метод выполняет такую долгую задачу, что за один HTTP-запрос от него нельзя сразу получить готовый ответ.
# Это может быть подсчет каких-то сложных вычислений или необходимость собрать информацию по разным источникам.
# В этом случае на первый запрос API начинает выполнения задачи, а на последующие ЛИБО говорит, что задача еще не готова,
# ЛИБО выдает результат. Сегодня я предлагаю протестировать такой метод.
# Сам API-метод находится по следующему URL: https://playground.learnqa.ru/ajax/api/longtime_job
url = 'https://playground.learnqa.ru/ajax/api/longtime_job'
# Если мы вызываем его БЕЗ GET-параметра token, метод заводит новую задачу, а в ответ выдает нам JSON со следующими полями:
#
# * seconds - количество секунд, через сколько задача будет выполнена
# * token - тот самый токен, по которому можно получить результат выполнения нашей задачи
#
# Если же вызвать метод, УКАЗАВ GET-параметром token, то мы получим следующий JSON:
#
# * error - будет только в случае, если передать token, для которого не создавалась задача. В этом случае в ответе будет следующая надпись - No job linked to this token
# * status - если задача еще не готова, будет надпись Job is NOT ready, если же готова - будет надпись Job is ready
# * result - будет только в случае, если задача готова, это поле будет содержать результат
#
# Наша задача - написать скрипт, который делал бы следующее:
#
# 1) создавал задачу
import requests
import time
response = requests.get(url)
print(response.json())
wait_time = int(response.json()['seconds'])
token = {"token": response.json()['token']}
# response = requests.get(url, params={"token": 'test'})
# print(response.json())

# 2) делал один запрос с token ДО того, как задача готова, убеждался в правильности поля status
response = requests.get(url, params=token)
print(response.text)
# 3) ждал нужное количество секунд с помощью функции time.sleep() - для этого надо сделать import time
time.sleep(wait_time+1)
# 4) делал бы один запрос c token ПОСЛЕ того, как задача готова, убеждался в правильности поля status и наличии поля result
response = requests.get(url, params=token)
if response.json()['status'] == 'Job is ready':
    print('Задача готова всё хорошо')
    print(response.text)
    print(response.json()['result'])
else:
    print('Запрос был выполнен слишком рано')
# Как всегда, код нашей программы выкладываем ссылкой на комит.