from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

opts = Options()
opts.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.3')
opts.add_argument('--headless') # para no abrir el navegador

driver = webdriver.Chrome(
  service=Service(ChromeDriverManager().install()), options=opts
)

# Hacemos la peticion inicial
driver.get('https://www.airbnb.mx/?_set_bev_on_new_domain=1706726793_ZWYyMTczZDdkYmZl')
sleep(3)

# Buscamos los elementos
titulos_anuncios = driver.find_elements(By.XPATH, '//div[@data-testid="listing-card-title"]')

for titulo in titulos_anuncios:
  print(titulo.text)