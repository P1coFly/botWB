import csv
from lib2to3.pgen2 import driver
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from datetime import datetime



url = "https://app.mpboost.pro/delivery"

option = webdriver.ChromeOptions()
option.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36')


phone ='+79959020721'
password = 'DKeouw'

action = ActionChains(driver)

def main():
    try:
        driver = webdriver.Chrome(
    executable_path='C:\\Users\\Art\\Desktop\\botwb\\script\\chromedriver.exe',
    options=option
    )
        
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
        time.sleep(3)
        
        #переходим к заказам
        driver.get(url=url)
        time.sleep(3)
        
        #Выбираем только заказы, которые готовы в выдаче
        driver.find_element(By.CLASS_NAME,"v-dropdown-menu__trigger").click()
        time.sleep(1)
        driver.find_element(By.XPATH,'//*[@id="root"]/div[1]/div/div[2]/div[1]/div[1]/div/div[2]/div[2]/div/ul/li[3]/button').click()
        time.sleep(3)
        
          
        #Скролим страницу до самого низа, чтобы подгрузились все заказы
        last_height = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        while True:
            # Скролим вниз
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Ждём прогрузку
            time.sleep(1)

            # Проверка на конец скрола
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            

        #t = driver.find_elements(By.CLASS_NAME,"delivery__header.delivery-header")
        #for test in t:
           # driver.execute_script("arguments[0].scrollIntoView();", test)
           # time.sleep(1)
            #test.click()
                          
        #сохраняем страницу
        with open('data.html','w', encoding="utf-8") as file:
            file.write(driver.page_source)
        
        time.sleep(3)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

def get_items(file_path):
    print("Обработка данных...")
    
    with open(file_path, encoding="utf-8") as file:
        src=file.read()
        
    soup = BeautifulSoup(src,'lxml')
    
    #Добываем Адрес, Получателя, Телефон и Код
    items_divs= soup.find_all("ul", class_="delivery__receiver receiver")
    
    #Добываем наименование товара
    products_divs = soup.find_all("table", class_="delivery__table table")
    
    #Достаём нужную информацию в List
    receivers = []
    phone = []
    address = []
    code = []
    for item in items_divs:
        item_receiver = item.find_all("span",class_="receiver__value")
        item_address = item.find_all("a",class_="receiver__value")
        
        receivers.append(item_receiver[0].text.strip())
        phone.append(item_receiver[1].text.strip())
        code.append(item_receiver[2].text.strip())
        
        address.append(item_address[0].text.strip().replace('\n','').replace('  ','').replace("'",""))
    
    product = []
    for prod in products_divs:
        item_product = prod.find_all("p",class_="cell__name")
        
        product.append(item_product[0].text.strip())
    
    #В качестве имени используем текующую дату
    filename_csv = f'{datetime.now().strftime("%m_%d_%Y_%H_%M")}.csv'
    
    #создаём csv с заголовками
    with open(filename_csv, 'w', encoding="cp1251", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        
        writer.writerow(
            (
                'Адрес',
                'Получатель',
                'Телефон',
                'Код',
                'Товар'
            )
        )
    
    #Собираем данные в одну строчку, чтобы съел csv
    result = list(zip(*[address,receivers,phone,code,product]))
    
    #Добавляем data в csv
    with open(filename_csv, 'a', encoding="cp1251", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        for r in result:
            writer.writerow(
                (
                r
                )
            )

    print(f'Файл {filename_csv} успешно создан!')
    

if __name__=='__main__':
    #main()
    get_items("data.html")