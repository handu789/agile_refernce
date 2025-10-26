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

#新智元 不加载图片 较快 部分一致 内容要少
base_time_str = "2025年6月2日"
base_time_format = "%Y年%m月%d日"
base_time = datetime.strptime(base_time_str, base_time_format)
driver_path = r'C:\Program Files\Google\Chrome\Application\chromedriver-win64\chromedriver.exe'
options = webdriver.ChromeOptions()
No_Image_loading = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", No_Image_loading)
options.add_argument("ignore-certificate-errors")
# 设置加载策略为eager
#options.page_load_strategy = 'none'
driver = webdriver.Chrome(executable_path=driver_path, options=options)
#https://aiera.com.cn/
url = 'http://aiera.com.cn/'
driver.get(url)
#element = driver.find_element(By.XPATH, '//*[@id="q"]')
#element.send_keys('巴以')
wait = random.uniform(1, 2)
time.sleep(wait)
js = 'window.scrollTo(0, 20000)'
driver.execute_script(js)
#driver.find_element(By.XPATH, '//*[@id="input-wrapper"]/span/button').click()
flag = 0
for j in range(5):
    for i in range(10):
        #//*[@id="main"]/div/section/div/article[1]/div/h2/a
        #//*[@id="main"]/div/section/div/article[2]/div/h2/a
        #//*[@id="main"]/div/section/div/article[3]/div/h2/a //*[@id="main"]/div[1]/header/ul[2]/li[2]/time
        url2 = driver.find_element(By.XPATH, '//*[@id="main"]/div/section/div/article[{}]/div/h2/a'.format(i + 1)).get_attribute('href')
        url2 = url2.replace('https', 'http')
        driver.execute_script("window.open('');")
        driver.switch_to_window(driver.window_handles[1])
        driver.get(url2)
        wait = random.uniform(1, 2)
        time.sleep(wait)
        try:
            title = driver.find_element(By.XPATH, '//*[@id="main"]/div[1]/header/h1').text
            content = driver.find_element(By.XPATH, '/html/body/div[2]/main/div[2]/article/div[1]').text
            time1 = driver.find_element(By.XPATH, '//*[@id="main"]/div[1]/header/ul[2]/li[2]/time').text
            entry_time = datetime.strptime(time1, base_time_format)
            if entry_time <= base_time:
                flag = 1
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
        df.to_csv(os.path.join(output_dir, 'xinzhiyuan.csv'), mode='a', encoding="utf-8-sig", index=False)
        wait = random.uniform(1, 2)
        time.sleep(wait)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        wait = random.uniform(1, 2)
        time.sleep(wait)
    if flag == 1:
        break
    if j + 1 == 1:
        url3 = driver.find_element(By.XPATH, '//*[@id="main"]/div/section/nav/a'.format(i + 1)).get_attribute('href')
    else:
        url3 = driver.find_element(By.XPATH, '//*[@id="main"]/div/section/nav/a[2]'.format(i + 1)).get_attribute('href')
    url3 = url3.replace('https', 'http')
    driver.get(url3)
        #if i + 1 == 1: //*[@id="main"]/div/section/nav/a //*[@id="main"]/div/section/nav/a[2]
            #driver.find_element(By.XPATH, '//*[@id="pageDiv"]/a[9]'.format(j + 1)).click()
        #elif i + 1 > 1 and i + 1 < 6:
            #driver.find_element(By.XPATH, '//*[@id="pageDiv"]/a[11]'.format(j + 1)).click()
        #else:
            #driver.find_element(By.XPATH, '//*[@id="pageDiv"]/a[13]'.format(j + 1)).click()