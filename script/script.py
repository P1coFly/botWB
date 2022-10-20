from lib2to3.pgen2 import driver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time



url = "https://app.mpboost.pro"

option = webdriver.ChromeOptions()
option.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36')
driver = webdriver.Chrome(
    executable_path='C:\\Users\\Art\\Desktop\\botwb\\script\\chromedriver.exe',
    options=option
    )

phone ='+79959020721'
password = 'DKeouw'

try:
    driver.get(url=url)
    time.sleep(5)
    
    #Вводим телефон
    phone_input=driver.find_element(By.NAME,'Phone')
    phone_input.clear
    phone_input.send_keys(phone)
    time.sleep(3)
    
    #Вводим пароль и нажимаем ENTER
    password_input = driver.find_element(By.NAME,'Password')
    password_input.clear
    password_input.send_keys(password)
    time.sleep(3)
    password_input.send_keys(Keys.ENTER)
    
    time.sleep(10)
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()