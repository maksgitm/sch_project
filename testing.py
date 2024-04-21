import requests


response = requests.post('https://metrika.mos.ru/hitcounter')
# response = response.json()
print(response.status_code)
