import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def obtener_script_scrolling(iteration, pxs = 2000):
  scrollingScript = 'window.scrollTo(0,2000)'
  return scrollingScript.replace('2000', str(pxs * iteration + 1))

opts = Options()
opts.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.3')

driver = webdriver.Chrome(service =  Service(ChromeDriverManager().install()), options=opts)

driver.get('https://www.youtube.com/playlist?list=PLuaGRMrO-j-8NndtkHMA7Y_7798tdJWKH')

sleep(2)

videos = driver.find_elements(By.XPATH, '//div[@id="contents"]/ytd-playlist-video-renderer')
urls_videos = []

for video in videos:
  url = video.find_element(By.XPATH, './/a[@id="video-title"]').get_attribute('href')

  urls_videos.append(url)

print(urls_videos)

# Vamos a cada url
for url in urls_videos:
  driver.get(url)
  sleep(2) 

  # Hacemos scroll
  driver.execute_script('window.scrollTo(0,400)')
  sleep(2)

  # Obtenemos la cantidad de comentarios 
  num_comments = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//h2[@id="count"]//span[1]'))
  )

  num_comments = int(num_comments.text) * 0.9

  comentarios_cargados = driver.find_elements(By.XPATH, '//ytd-comment-renderer[@id="comment"]')

  # Hacemos scroll mientras los comentarios cargados sea menor a el 90 %
  n_scrolls = 1
  n_scrolls_max = 5
  while len(comentarios_cargados) < num_comments and n_scrolls < n_scrolls_max:
    driver.execute_script(obtener_script_scrolling(n_scrolls))
    n_scrolls += 1
    sleep(2)

    comentarios_cargados = driver.find_elements(By.XPATH, '//ytd-comment-renderer[@id="comment"]')

  for comentario in comentarios_cargados:
    txt = comentario.text
    print(txt)

  print('------------\n')