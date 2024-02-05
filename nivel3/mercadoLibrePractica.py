import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Parametros de scraping
PRODUCT = 'balones futbol'
NAME_FILE = 'balones.csv'
MAX_PAGES = 10
objects_finded = []


# Mientras mas escrolls llevo dando, mas pixeles voy bajando
# Para esto utilizo el scrolling que voy haciendo actualmente para bajar hasta cierta posicion en la pagina
def hacer_scrolling_suavizado(driver, iteracion):
    bajar_hasta = 2000 * (iteracion + 1)
    inicio = (iteracion * 2000) # Inicio donde termine la anterior iteracion
    for i in range(inicio,  bajar_hasta, 5): # Cada vez avanzo 5 pixeles
        scrollingScript = f""" 
          window.scrollTo(0, {str(i)})
        """
        driver.execute_script(scrollingScript)

opts = Options()
opts.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.3')

driver = webdriver.Chrome(service =  Service(ChromeDriverManager().install()), options=opts)

# Hacemos la petición a mercadolibre
driver.get('https://www.mercadolibre.com.mx/')

# Seleccionamos el buscador
search_input = driver.find_element(By.XPATH, '//input[@class="nav-search-input"]')
# Seleccionamos el boton de busqueda
search_button = driver.find_element(By.XPATH, '//button[@class="nav-search-btn"]')
# Seleccionamos el boton de cockies
coockies_button = driver.find_element(By.XPATH, '//button[text()="Aceptar cookies"]')

# Hacemos la busqueda
search_input.send_keys(PRODUCT)

try:
  coockies_button.click()
  sleep(0.1)
  search_button.click()
except:
  print('Error al cliquear boton de busqueda')

pages_counter = 0

while pages_counter < MAX_PAGES:
  """ sleep(1.5)
  # Hacemos scroll
  for i in range(7):
    hacer_scrolling_suavizado(driver, i) """

  # Obtenemos los elementos:
  articles = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, '//ol//li[@class="ui-search-layout__item"]'))
  )

  for article in articles:
    title = article.find_element(By.XPATH, './/h2').text
    price = article.find_element(By.XPATH, './/div[@class="ui-search-price__second-line"]//span[@class="andes-money-amount__fraction"]').text
    # No todos los articulos tienen calificación
    rating = '-'
    try:
      rating = article.find_element(By.XPATH, './/div[contains(@class, "ui-search-reviews ")]//span[@class="ui-search-reviews__rating-number"]').text
    except:
      rating = '-'

    objects_finded.append({
      'title': title,
      'price': price,
      'rating': rating
    })

  try:
    # Siguiente página
    next_button = WebDriverWait(driver, 5).until(
      EC.presence_of_element_located((By.XPATH, '//li[contains(@class, "andes-pagination__button--next")]'))
    )

    next_button.click()
    pages_counter += 1
  except Exception as e:
    print(e)
    break

# Exportamos la data recolectada
df = pd.DataFrame(objects_finded)
df.to_csv(NAME_FILE)