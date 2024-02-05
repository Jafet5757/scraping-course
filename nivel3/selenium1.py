import random
from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver # pip install selenium
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Asi podemos setear el user-agent en selenium
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.3")

# driver de selenium para el navegador
driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=opts)


# Hacemos la peticion
driver.get('https://www.olx.in/cars_c84')
sleep(2)
driver.refresh() # Solucion de un bug extraño en Windows en donde los anuncios solo cargan al hacerle refresh a la página
sleep(2) # Esperamos que cargue el boton

# cargamos más elementos haciendo click en le botón
for i in range(3):
  try:
    # Esperamos que el botón se cargue y clickeamos
    boton = WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.XPATH, '//button[@data-aut-id="btnLoadMore"]'))
    )
    # hacemos click
    boton.click()
    print('click')
    # esperamos a que aparezca la info
    WebDriverWait(driver, 10).until(
      EC.presence_of_all_elements_located((By.XPATH, '//li[@data-aut-id="itemBox"]//span[@data-aut-id="itemPrice"]'))
    )
  except:
    break


# Obtenemos los elementos
autos = driver.find_elements(By.XPATH, '//li[@data-aut-id="itemBox"]')
c = 0

for auto in autos:
  try:
    precio = auto.find_element(By.XPATH, './/span[@data-aut-id="itemPrice"]').text
    print(precio)
    descripcion = auto.find_element(By.XPATH, './/div[@data-aut-id="itemTitle"]').text
    print(descripcion)
    c += 1
  except Exception as e:
    print ('Anuncio carece de precio o descripcion')

print('Total: ', c)