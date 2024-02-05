import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


scrollingScript = """ 
      document.getElementsByClassName('m6QErb DxyBCb kA9KIf dS8AEf')[0].scroll(0, 20000)
    """

opts = Options()
opts.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.3')

driver = webdriver.Chrome(service =  Service(ChromeDriverManager().install()), options=opts)

driver.get("https://www.google.com/maps/place/Amaz%C3%B3nico/@40.423706,-3.6872655,17z/data=!4m8!3m7!1s0xd422899dc90366b:0xce28a1dc0f39911d!8m2!3d40.423715!4d-3.6850997!9m1!1b1!16s%2Fg%2F11df4t5hhs?entry=ttu")

sleep(random.uniform(4,6))

# Hacemos el scrolling
SCROLLS = 0
while SCROLLS != 3:
  driver.execute_script(scrollingScript)
  sleep(random.uniform(5,6))
  SCROLLS += 1

reviews_restaurante = driver.find_elements(By.XPATH, "//div[contains(@class, 'jftiEf fontBodyMedium ')]")

for review in reviews_restaurante:
  userLink = review.find_element(By.XPATH, './/button[contains(@class, "al6Kxe")]')

  # Hacemos click al perfil
  try:
    # Cambiamos de pestaña
    userLink.click()
    driver.switch_to.window(driver.window_handles[1])

    # Essperamos a que carge el contenedor
    WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "m6QErb DxyBCb kA9KIf dS8AEf ")]'))
    )

    USER_SCROLLS = 0
    while(USER_SCROLLS != 3):
      driver.execute_script(scrollingScript)
      sleep(random.uniform(5,6))
      USER_SCROLLS += 1

    user_reviews = driver.find_elements(By.XPATH, "//div[contains(@class, 'jftiEf fontBodyMedium')]")

    for r in user_reviews:
      description = r.find_element(By.XPATH, './/div[@class="MyEned"]//span[@class="wiI7pd"]').text
      rating = r.find_element(By.XPATH, './/span[@class="kvMYJc"]').get_attribute('aria-label')

      print(description)
      print(rating)

    # Cierra la pestaña
    driver.close()
    # nos movemos a la pestaña cero
    driver.switch_to.window(driver.window_handles[0])

  except Exception as e:
    print(e)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])