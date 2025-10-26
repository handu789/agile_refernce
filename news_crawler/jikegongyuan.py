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

#极客公园 快 一致 内容要多
base_time_str = "2025/06/02"
base_time_format = "%Y/%m/%d"
base_time = datetime.strptime(base_time_str, base_time_format)
driver_path = r'C:\Program Files\Google\Chrome\Application\chromedriver-win64\chromedriver.exe'
options = webdriver.ChromeOptions()
No_Image_loading = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", No_Image_loading)
options.add_argument("ignore-certificate-errors")
driver = webdriver.Chrome(executable_path=driver_path, options=options)
#https://www.geekpark.net/column/179
#https://www.geekpark.net/column/304
#https://www.geekpark.net/column/2
#https://www.geekpark.net/column/74
url = 'https://www.geekpark.net/column/179'
driver.get(url)
#element = driver.find_element(By.XPATH, '//*[@id="q"]')
#element.send_keys('巴以')
wait = random.uniform(1, 2)
time.sleep(wait)
js = 'window.scrollTo(0, 20000)'
driver.execute_script(js)
driver.find_element(By.XPATH, '//*[@id="column"]/div[3]/div/div[2]/div/a').click()
js = 'window.scrollTo(0, 20000)'
driver.execute_script(js)
for i in range(20):
    #//*[@id="column"]/div[3]/div/div[2]/article[2]/div[1]/a[2]
    #//*[@id="column"]/div[3]/div/div[2]/article[3]/div[1]/a[2]
    #//*[@id="categories-show"]/div[5]/div/div/div/span[1]/div[2]/div[1]/div[1]/article
    driver.find_element(By.XPATH, '//*[@id="column"]/div[3]/div/div[2]/article[{}]/div[1]/a[2]'.format(i + 1)).click()
    driver.switch_to_window(driver.window_handles[1])
    wait = random.uniform(1, 2)
    time.sleep(wait)
    try:
        title = driver.find_element(By.XPATH, '//*[@id="post"]/section/div/article/header/h1').text
        content = driver.find_element(By.XPATH, '//*[@id="article-body"]').text
        time1 = driver.find_element(By.XPATH, '//*[@id="post"]/section/div/article/header/div[2]/span').text
        entry_time = datetime.strptime(time1, base_time_format)
        if entry_time <= base_time:
            print('=========时间到=========')
            break
    except:
        try:
            title = driver.find_element(By.XPATH, '//*[@id="post"]/section/div/article/header/h1').text
            content = driver.find_element(By.XPATH, '//*[@id="article-body"]').text
            time1 = driver.find_element(By.XPATH, '//*[@id="post"]/section/div/article/header/div/span').text
            entry_time = datetime.strptime(time1, base_time_format)
            if entry_time <= base_time:
                print('=========时间到=========')
                break
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
    df.to_csv(os.path.join(output_dir, 'jikegongyuan.csv'), mode='a', encoding="utf-8-sig", index=False)
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