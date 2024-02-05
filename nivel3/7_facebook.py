import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


# Mientras mas escrolls llevo dando, mas pixeles voy bajando
# Para esto utilizo el scrolling que voy haciendo actualmente para bajar hasta cierta posicion en la pagina
def hacer_scrolling_suavizado(driver, iteracion):
    bajar_hasta = 2000 * (iteracion + 1)
    inicio = (iteracion * 2000) # Inicio donde termine la anterior iteracion
    for i in range(inicio,  bajar_hasta, 5): # Cada vez avanzo 5 pixeles
        scrollingScript = f""" 
          window.scrollTo(0, {i})
        """
        driver.execute_script(scrollingScript)

opts = Options()
opts.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.3')

driver = webdriver.Chrome(service =  Service(ChromeDriverManager().install()), options=opts)

# Hacemos la petición
driver.get('https://www.facebook.com/elcorteingles')

# Obtenemos el botón de cerrar
close_button = WebDriverWait(driver, 10).until(
  EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Cerrar"]'))
)

# Cliqueamos
try:
  close_button.click()
except:
  print('Click error')

posts = driver.find_elements(By.XPATH, '//div[@aria-posinset and @aria-describedby]')

n_scrolls = 0
max_scrolls = 10
max_posts = 50

while len(posts) < max_posts and n_scrolls < max_scrolls:
  hacer_scrolling_suavizado(driver, n_scrolls)
  n_scrolls += 1
  posts = driver.find_elements(By.XPATH, '//div[@aria-posinset and @aria-describedby]')
  sleep(2)

  posts = driver.find_elements(By.XPATH, '//div[@aria-posinset and @aria-describedby]')

  for post in posts:
    reactions = post.find_element(By.XPATH, './/span[@class="x1e558r4"]').text
    commentsAndShares = post.find_elements(By.XPATH, './/span[@class="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xi81zsa"]')
    cas = []
    for c in commentsAndShares:
      cas.append(c.text)
    print('Reacciones: ', reactions)
    print('C:', cas)
    print('\n')