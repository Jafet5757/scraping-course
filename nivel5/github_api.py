import requests
import json

endpoint = 'https://api.github.com/user/repos?page=0'


usuario = 'jafet5757'
password = ''

response = requests.get(endpoint, auth=(usuario, password))

print(response.json())