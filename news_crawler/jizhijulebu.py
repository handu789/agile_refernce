from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from selenium.webdriver.common.keys import Keys
import json
import pandas as pd
from datetime import datetime, timedelta
import os

#集智俱乐部 快 一致
base_time_str = "2025-06-02"
base_time_format = "%Y-%m-%d"
base_time = datetime.strptime(base_time_str, base_time_format)
driver_path = r'C:\Program Files\Google\Chrome\Application\chromedriver-win64\chromedriver.exe'
options = webdriver.ChromeOptions()
No_Image_loading = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", No_Image_loading)
options.add_argument("ignore-certificate-errors")
driver = webdriver.Chrome(executable_path=driver_path, options=options)
url = 'https://swarma.org/'
driver.get(url)
#element = driver.find_element(By.XPATH, '//*[@id="q"]')
#element.send_keys('巴以')
wait = random.uniform(1, 2)
time.sleep(wait)
#driver.find_element(By.XPATH, '//*[@id="fa-loadmore"]').click()
for i in range(10):
    #//*[@id="page-content"]/div/div/div/div[1]/div[1]/li[10]/div/div[2]/h2/a
    #//*[@id="page-content"]/div/div/div/div[1]/div[1]/div[3]/div/div[2]/h2/a
    #//*[@id="page-content"]/div/div/div/div[1]/div[1]/li[1]/div/div[2]/h2/a
    driver.find_element(By.XPATH, '//*[@id="page-content"]/div/div/div/div[1]/div[1]/div[{}]/div/div[2]/h2/a'.format(i + 1)).click()
    driver.switch_to_window(driver.window_handles[1])
    wait = random.uniform(1, 2)
    time.sleep(wait)
    try:
        title = driver.find_element(By.XPATH, '//*[@id="page-content"]/div/div/div[1]/div[1]/div[1]/h1').text
        content = driver.find_element(By.XPATH, '//*[@id="page-content"]/div/div/div[1]/div[1]/div[2]').text
        time1 = driver.find_element(By.XPATH, '//*[@id="page-content"]/div/div/div[1]/div[1]/div[1]/div/span[1]').text
        try:
            entry_time = datetime.strptime(time1, base_time_format)
            if entry_time <= base_time:
                print('=========时间到=========')
                break
        except:
            time1 = "2025-06-02"
    except:
        try:
            title = driver.find_element(By.XPATH, '//*[@id="playerwrap"]/div[1]/div[1]').text
            content = driver.find_element(By.XPATH, '//*[@id="playerwrap"]/div[3]').text
        except:
            print('=========元素位置出错=========')
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            wait = random.uniform(1, 2)
            time.sleep(wait)
            continue
    url = driver.current_url
    news = []
    news.append({"title":title, "time":time1, "href":url,"passage":content})
    df=pd.DataFrame(news)
    df.to_csv('tech_news/20250421/jizhijulebu.csv',mode='a', encoding="utf-8",index=False)
    wait = random.uniform(1, 2)
    time.sleep(wait)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    js = 'window.scrollTo(0, 5000)'
    driver.execute_script(js)
    wait = random.uniform(1, 2)
    time.sleep(wait)

driver.find_element(By.XPATH, '//*[@id="fa-loadmore"]').click()
wait = random.uniform(1, 2)
time.sleep(wait)
for j in range(10):
    #//*[@id="page-content"]/div/div/div/div[1]/div[1]/li[1]/div/div[2]/h2/a
    #//*[@id="page-content"]/div/div/div/div[1]/div[1]/li[2]/div/div[2]/h2/a
    #//*[@id="page-content"]/div/div/div/div[1]/div[1]/li[1]/div/div[2]/h2/a
    url2 = driver.find_element(By.XPATH, '//*[@id="page-content"]/div/div/div/div[1]/div[1]/li[{}]/div/div[2]/h2/a'.format(j + 1)).get_attribute('href')
    url2 = url2.replace('https', 'http')
    driver.execute_script("window.open('');")
    driver.switch_to_window(driver.window_handles[1])
    driver.get(url2)
    wait = random.uniform(1, 2)
    time.sleep(wait)
    try:
        title = driver.find_element(By.XPATH, '//*[@id="page-content"]/div/div/div[1]/div[1]/div[1]/h1').text
        content = driver.find_element(By.XPATH, '//*[@id="page-content"]/div/div/div[1]/div[1]/div[2]').text
        time1 = driver.find_element(By.XPATH, '//*[@id="page-content"]/div/div/div[1]/div[1]/div[1]/div/span[1]').text
        try:
            entry_time = datetime.strptime(time1, base_time_format)
            if entry_time <= base_time:
                print('=========时间到=========')
                break
        except:
            time1 = "2025-04-21"
    except:
        try:
            title = driver.find_element(By.XPATH, '//*[@id="playerwrap"]/div[1]/div[1]').text
            content = driver.find_element(By.XPATH, '//*[@id="playerwrap"]/div[3]').text
        except:
            print('=========元素位置出错=========')
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            wait = random.uniform(1, 2)
            time.sleep(wait)
            continue
    url = driver.current_url
    news = []
    news.append({"title":title, "time":time1, "href":url,"passage":content})
    df=pd.DataFrame(news)
    output_dir = 'tech_news/20250421'
    os.makedirs(output_dir, exist_ok=True)
    df.to_csv(os.path.join(output_dir, 'jizhijulebu.csv'), mode='a', encoding="utf-8-sig", index=False)
    wait = random.uniform(1, 2)
    time.sleep(wait)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    js = 'window.scrollTo(0, 5000)'
    driver.execute_script(js)
    wait = random.uniform(1, 2)
    js = 'window.scrollTo(0, 5000)'
    driver.execute_script(js)
    wait = random.uniform(1, 2)
    time.sleep(wait)