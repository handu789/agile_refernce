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

#量子位 不加载图片 较快 /feed 大部分一致 内容要多
base_time_str = "2025-06-02"
base_time_format = "%Y-%m-%d"
base_time = datetime.strptime(base_time_str, base_time_format)
driver_path = r'C:\Program Files\Google\Chrome\Application\chromedriver-win64\chromedriver.exe'
options = webdriver.ChromeOptions()
#options.add_argument('--headless')  # 将无头模式添加到ChromeOptions
No_Image_loading = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", No_Image_loading)
options.add_argument("ignore-certificate-errors")
driver = webdriver.Chrome(executable_path=driver_path, options=options)
# 设置加载策略为eager
#options.page_load_strategy = 'none'
#driver = webdriver.Chrome()
#https://www.qbitai.com/category/%e8%b5%84%e8%ae%af
#https://www.qbitai.com/category/auto
url = 'https://www.qbitai.com/category/auto'
driver.get(url)
'''driver.set_page_load_timeout(8)
try:
    url = 'https://www.qbitai.com/category/%e8%b5%84%e8%ae%af'
    driver.get(url)
except:
    driver.execute_script('window.stop()')'''
#element = driver.find_element(By.XPATH, '//*[@id="q"]')
#element.send_keys('巴以')
wait = random.uniform(1, 2)
time.sleep(wait)
js = 'window.scrollTo(0, 20000)'
driver.execute_script(js)
#//*[@id="more_news"]
driver.find_element(By.XPATH, '//*[@id="more_news"]').click()
wait = random.uniform(1, 2)
time.sleep(wait)
js = 'window.scrollTo(0, 20000)'
driver.execute_script(js)
driver.find_element(By.XPATH, '//*[@id="more_news"]').click()
wait = random.uniform(1, 2)
time.sleep(wait)
js = 'window.scrollTo(0, 20000)'
driver.execute_script(js)
#driver.set_page_load_timeout(300)
for i in range(35):
    #/html/body/div[1]/div[1]/div/div[2]/div[2]/h4/a
    #/html/body/div[1]/div[1]/div/div[1]/div[2]
    #/html/body/div[1]/div[1]/div/div[1]/div[2]/h4/a
    #driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div[{}]/div[2]/h4/a'.format(i + 1)).click()
    url2 = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div[{}]/div[2]/h4/a'.format(i + 1)).get_attribute('href')
    driver.execute_script("window.open('');")
    driver.switch_to_window(driver.window_handles[1])
    driver.get(url2)
    wait = random.uniform(1, 2)
    time.sleep(wait)
    try:
        title = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/h1').text
        content = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]').text
        time1 = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/span[2]').text
        entry_time = datetime.strptime(time1, base_time_format)
        if entry_time <= base_time:
            print('=========时间到=========')
            break
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
    df.to_csv(os.path.join(output_dir, 'liangziwei.csv'), mode='a', encoding="utf-8-sig", index=False)
    wait = random.uniform(1, 2)
    time.sleep(wait)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    wait = random.uniform(1, 2)
    time.sleep(wait)
    #if i + 1 == 1:
        #driver.find_element(By.XPATH, '//*[@id="pageDiv"]/a[9]'.format(j + 1)).click()
    #elif i + 1 > 1 and i + 1 < 6:
        #driver.find_element(By.XPATH, '//*[@id="pageDiv"]/a[11]'.format(j + 1)).click()
    #else:
        #driver.find_element(By.XPATH, '//*[@id="pageDiv"]/a[13]'.format(j + 1)).click()