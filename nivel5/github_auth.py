import requests # hace petitiones a la web
from lxml import html # para parsear el html

# cambiamos el user-agent para que no nos bloquee la web
headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0'
}

url = "https://github.com/login"
login_url = 'https://github.com/session'

session = requests.Session()

form_res = session.get(url, headers=headers)

parser = html.fromstring(form_res.content)
token = parser.xpath('//input[@name="authenticity_token"]/text()')

login_data = {
  'login': 'jafet5757',
  'password': '',
  'commit': 'Sign in',
  'authenticity_token': token
}

session.post(
  login_url,
  data=login_data,
  headers=headers
)