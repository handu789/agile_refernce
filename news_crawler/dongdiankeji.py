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
#动点科技 快 /feed 部分一致 内容要多 基本新闻一致
base_time_str = "2025/06/02 00:00"
base_time_format = "%Y/%m/%d %H:%M"
base_time = datetime.strptime(base_time_str, base_time_format)
driver_path = r'C:\Program Files\Google\Chrome\Application\chromedriver-win64\chromedriver.exe'
options = webdriver.ChromeOptions()
No_Image_loading = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", No_Image_loading)
options.add_argument("ignore-certificate-errors")
driver = webdriver.Chrome(executable_path=driver_path, options=options)
url = 'https://cn.technode.com/post/category/consumertech/'
driver.get(url)
#element = driver.find_element(By.XPATH, '//*[@id="q"]')
#element.send_keys('巴以')
wait = random.uniform(1, 2)
time.sleep(wait)
js = 'window.scrollTo(0, 20000)'
driver.execute_script(js)
flag = 0
#driver.find_element(By.XPATH, '//*[@id="input-wrapper"]/span/button').click()
for j in range(3):
    for i in range(12):
        #/html/body/div[3]/div/div[2]/div/div/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div/div[2]/div/div/h3/a
        #/html/body/div[3]/div/div[2]/div/div/div/div/div/div[1]/div/div/div/div/div/div/div[3]/div/div[2]/div/div/h3/a
        #//*[@id="main"]/div/section/div/article[3]/div/h2/a
        url2 = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div/div/div/div/div[1]/div/div/div/div/div/div/div[{}]/div/div[2]/div/div/h3/a'.format(i + 1)).get_attribute('href')
        driver.execute_script("window.open('');")
        driver.switch_to_window(driver.window_handles[1])
        driver.get(url2)
        wait = random.uniform(1, 2)
        time.sleep(wait)
        try:
            title = driver.find_element(By.XPATH, '//*[@id="page-header"]/div/div/div[2]/div/div/h1/span').text
            content = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div/div/article/div/div[1]/div/div/div/div[1]/div').text
            time1 = driver.find_element(By.XPATH, '//*[@id="page-header"]/div/div/div[2]/div/div/div/div[1]').text
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
        df.to_csv(os.path.join(output_dir, 'dongdiankeji.csv'), mode='a', encoding="utf-8-sig", index=False)
        wait = random.uniform(1, 2)
        time.sleep(wait)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        wait = random.uniform(1, 2)
        time.sleep(wait)
    if flag == 1:
        break
    if j + 1 == 1:
        #/html/body/div[3]/div/div[2]/div/div/div/div/div/div[2]/div/ul/li[8]/a /html/body/div[3]/div/div[2]/div/div/div/div/div/div[2]/div/ul/li[9]/a
        url3 = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div/div/div/div/div[2]/div/ul/li[7]/a'.format(i + 1)).get_attribute('href')
    elif j + 1 == 2:
        url3 = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div/div/div/div/div[2]/div/ul/li[8]/a'.format(i + 1)).get_attribute('href')
    elif j + 1 == 3:
        url3 = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div/div/div/div/div[2]/div/ul/li[9]/a'.format(i + 1)).get_attribute('href')
    driver.get(url3)
        #if i + 1 == 1: //*[@id="main"]/div/section/nav/a //*[@id="main"]/div/section/nav/a[2]
            #driver.find_element(By.XPATH, '//*[@id="pageDiv"]/a[9]'.format(j + 1)).click()
        #elif i + 1 > 1 and i + 1 < 6:
            #driver.find_element(By.XPATH, '//*[@id="pageDiv"]/a[11]'.format(j + 1)).click()
        #else:
            #driver.find_element(By.XPATH, '//*[@id="pageDiv"]/a[13]'.format(j + 1)).click()