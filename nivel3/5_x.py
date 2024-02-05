import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


opts = Options()
opts.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.3')

driver = webdriver.Chrome(service =  Service(ChromeDriverManager().install()), options=opts)

driver.get('https://twitter.com/home')

USER = 'moranorozcokevinjafet@gmail.com'
PASSWORD = '8J3$90@f@%sdOC^UwQ'

input_driver = WebDriverWait(driver, 10).until(
  EC.presence_of_element_located((By.XPATH, '//input'))
)
next_button = driver.find_element(By.XPATH, '//span[text()="Siguiente"]')

# Llenamos el campo usuario
input_driver.send_keys(USER)

# Cliqueamos en siguiente
try:
  next_button.click()
  input_password = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//input[@name="password"]'))
  )
  # Agregamos la contraseña
  input_password.send_keys(PASSWORD)
  # Obtenemos el boton de inicio
  login_button = driver.find_element(By.XPATH, '//span[text()="Iniciar sesión"]')
  # CLICKEAMOS
  login_button.click() 
except Exception as e:
  print(e)

# Obtenemos los articulos
articles = WebDriverWait(driver, 10).until(
  EC.presence_of_all_elements_located((By.XPATH, '//div[@data-testid="cellInnerDiv"]'))
)

# Obtenemos el time de cada articulo
for article in articles:
  time = article.find_element(By.XPATH, './/time').text
  print(time)