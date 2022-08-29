import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller

url = "https://www.cafe24.com/"
id = "nslifill"
password = "fkdlvlf11@@"

options = webdriver.ChromeOptions()

# options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("lang=en")
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36')
# options.add_extension('C:/Users/user/Desktop/자동화/njmehopjdpcckochcggncklnlmikcbnb-6.8.7-Crx4Chrome.com.crx')
options.add_extension('C:/Users/user/Desktop/자동화/fjoaledfpmneenckfbpdfhkmimnjocfa.crx')
# options.add_argument = {"user-data-dir":"C:/Users/user/Chrome/Default"}
# options.add_argument = {"user-data-dir":"C:/Users/user/UserData/Default"}


# Chrome Driver 자동 Download
chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
chrome_filename = chromedriver_autoinstaller.utils.get_chromedriver_filename()

CHROMEDRIVER = f"./{chrome_ver}/{chrome_filename}"

chrome_service = fs.Service(executable_path=CHROMEDRIVER)
browser = webdriver.Chrome(service=chrome_service, options=options)

browser.get(url)

time.sleep(1)

browser.find_element(By.XPATH, '//*[@id="header"]/div[2]/div[3]/div[2]/div/a[2]').click()

time.sleep(1)

browser.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div/div/ul[1]/li[1]/div/div/a').click()

time.sleep(5)

browser.switch_to.window(browser.window_handles[1])

browser.find_element(By.CSS_SELECTOR, '#mall_id').send_keys(id)

browser.find_element(By.CSS_SELECTOR, '#userpasswd').send_keys(password)

browser.find_element(By.CSS_SELECTOR, '#userpasswd').send_keys(Keys.ENTER)

time.sleep(30)








