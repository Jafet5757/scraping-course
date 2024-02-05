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

driver.get('https://www.google.com/recaptcha/api2/demo')

try:
  # nos movemos al iframe
  driver.switch_to.frame(driver.find_element(By.XPATH, '//iframe'))

  captcha = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.XPATH, '//div[@class="recaptcha-checkbox-border"]'))
  )
  captcha.click()

  print('Press enter to continue')
  input()

  # salimos del iframe
  driver.switch_to.default_content()

  # Presionamos el botón de submit
  submit_button = driver.find_element(By.XPATH, '//input[@id="recaptcha-demo-submit"]')
  submit_button.click()
except Exception as e:
  print(e)


sleep(5)