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

driver.get('https://listado.mercadolibre.com.mx/listado-herramientas-vehiculos?internal_referrer=true&matt_tool=6166775&matt_word=SEARCH')


while True:
  links_productos = driver.find_elements(By.XPATH, '//a[@class="ui-search-item__group__element ui-search-link__title-card ui-search-link"]')

  links_pagina = []

  # Obtenemos los enlaces
  for tag_a in links_productos:
    print(tag_a)
    links_pagina.append(tag_a.get_attribute('href'))

  # Visitamos los enlaces
  for link in links_pagina:
    try:
      driver.get(link)
      titulo = driver.find_element(By.XPATH, '//h1').text
      precio = driver.find_element(By.XPATH, '//span[@class="andes-money-amount__fraction"]').text
      print(titulo)
      print(precio)
      driver.back()
    except Exception as e:
      print(e)
      driver.back()

  try: 
    boton_siguiente = driver.find_element(By.XPATH, '//span[text()="Siguiente"]')
    boton_siguiente.click()
    print('click')
  except Exception as e:
    print(e)
    break