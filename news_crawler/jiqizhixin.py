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
#机器之心 快 一致
base_time_str = "6月2日"
base_time_format = "%m月%d日"
base_time = datetime.strptime(base_time_str, base_time_format)
base_time_now = datetime.strptime('6月2日', base_time_format)
driver_path = r'C:\Program Files\Google\Chrome\Application\chromedriver-win64\chromedriver.exe'

options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 将无头模式添加到ChromeOptions
No_Image_loading = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", No_Image_loading)
options.add_argument("ignore-certificate-errors")
driver = webdriver.Chrome(executable_path=driver_path, options=options)
#driver = webdriver.Chrome(options=options)
#driver = webdriver.Chrome()
#https://www.jiqizhixin.com/categories/basic
#https://www.jiqizhixin.com/categories/theory
#https://www.jiqizhixin.com/categories/practice
url = 'https://www.jiqizhixin.com/categories/practice'
driver.get(url)
#element = driver.find_element(By.XPATH, '//*[@id="q"]')
#element.send_keys('巴以')
wait = random.uniform(3, 5)
time.sleep(wait)
js = 'window.scrollTo(0, 20000)'
driver.execute_script(js)
#driver.find_element(By.XPATH, '//*[@id="input-wrapper"]/span/button').click()
for i in range(30):
    #//*[@id="categories-show"]/div[2]/div/div/div/span[1]/div[2]/div[1]/div[15]/article/main/a
    #//*[@id="categories-show"]/div[5]/div/div/div/span[1]/div[2]/div[1]/div[2]/article/main/a
    #//*[@id="article_library"]/div/div/div[2]/div/div/div[3]/div[1]/p
    driver.find_element(By.XPATH, '//*[@id="categories-show"]/div[2]/div/div/div/span[1]/div[2]/div[1]/div[{}]/article'.format(i + 1)).click()
    driver.switch_to_window(driver.window_handles[1])
    wait = random.uniform(2, 3)
    time.sleep(wait)
    try:
        title = driver.find_element(By.XPATH, '//*[@id="article_library"]/div/div/div[2]/div/div/div[3]/div[1]/p').text
        content = driver.find_element(By.XPATH, '//*[@id="article_library"]/div/div/div[2]/div/div/div[3]/div[2]').text
        time1 = driver.find_element(By.XPATH, '//*[@id="article_library"]/div/div/div[2]/div/div/div[3]/div[1]/div/div/p').text
        print(time1)
        try:
            entry_time = datetime.strptime(time1, base_time_format)
            if entry_time <= base_time:
                print('=========时间到=========')
                break
        except:
            delta = 0 - 1
            if '天' in time1:
                delta = int(list(time1)[0]) - 1
            print(delta)
            base_time1 = base_time_now - timedelta(days=delta)
            time1 = base_time1.strftime('%m{M}%d{D}').format(M='月', D='日')
    except Exception as e:
        print(e)
        try:
            title = driver.find_element(By.XPATH, '//*[@id="playerwrap"]/div[1]/div[1]').text
            #print(title)
            content = driver.find_element(By.XPATH, '//*[@id="playerwrap"]/div[3]').text
            #print(content)
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
    df.to_csv(os.path.join(output_dir, 'jiqizhixin.csv'), mode='a', encoding="utf-8-sig", index=False)
    wait = random.uniform(1, 2)
    time.sleep(wait)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    wait = random.uniform(1, 2)
    time.sleep(wait)
    if i + 1 == 20:
        js = 'window.scrollTo(0, 20000)'
        driver.execute_script(js)
    #if i + 1 == 1:
        #driver.find_element(By.XPATH, '//*[@id="pageDiv"]/a[9]'.format(j + 1)).click()
    #elif i + 1 > 1 and i + 1 < 6:
        #driver.find_element(By.XPATH, '//*[@id="pageDiv"]/a[11]'.format(j + 1)).click()
    #else:
        #driver.find_element(By.XPATH, '//*[@id="pageDiv"]/a[13]'.format(j + 1)).click()