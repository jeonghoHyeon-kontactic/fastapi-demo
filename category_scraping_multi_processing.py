from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import chromedriver_autoinstaller
import os
import glob
import pandas as pd
import time
from pathos.multiprocessing import ProcessingPool as Pool

class CategoryScraping:

    def __init__(self, type):
        self.type = type
        self.url = "https://www.amazon.com/dp/{}"
        self.asins = []
        self.category_list = []
        self.download_directory = 'C:/Users/user/Downloads/'
        self.processingCnt = 0

    # 멀티프로세싱
    def multi_processing(self):
        options = webdriver.ChromeOptions()

        # options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("lang=en")
        options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36')
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

    # csv 파일 병합
    def combine_csv(self):
        # 다운로드 경로에 있는 csv 파일을 모두 가지고 온다.
        all_file_list = glob.glob(os.path.join(self.download_directory, '*.csv'))
        print("파일 개수 : {}개".format(len(all_file_list)))

        # 읽어 들인 csv파일 내용을 저장할 빈 리스트를 하나 만든다.
        allData = []

        for file in all_file_list:
            # CSV파일 읽기
            df = pd.read_csv(file)

            # 빈 리스트에 읽어 들인 내용을 추가
            allData.append(df)

            # # # 기존에 있던 csv 파일 삭제
            # os.remove(file)

        # 모든 csv 파일 내용 병합
        dataCombine = pd.concat(allData, axis=0, ignore_index=True)
        print("파일 병합 후 ASIN : {}개".format(len(dataCombine.index)))

        # ASIN 기준으로 중복 제거
        dataCombine = dataCombine.drop_duplicates(['ASIN'], keep='last')
        print("중복 제거 후 ASIN : {}개".format(len(dataCombine.index)))

        # sales / price / revenue 중 n/a 인 row 삭제
        dataCombine = dataCombine.dropna(axis=0, how='any', subset='Sales')

        dataCombine = dataCombine.dropna(axis=0, how='any', subset='Price $')

        dataCombine = dataCombine.dropna(axis=0, how='any', subset='Revenue')

        print("n/a 제거 후 ASIN : {}개".format(len(dataCombine.index)))

        # 광고 리스팅 삭제
        dfresult = dataCombine[~dataCombine['Product Details'].str.startswith('($)')]

        print("광고 제거 후 ASIN : {}개".format(len(dfresult)))

        self.asins = dfresult['ASIN']

        self.result = dfresult

        self.pool = Pool(processes=4)
        self.pool.map(self.scraping_category,self.asins)


    def scraping_category(self):

        for asin in self.asins:

            if self.check_asin_count(asin) == True:

                detail_category = BeautifulSoup(self.browser.page_source, 'lxml').find_all('a', attrs={"class",
                                                                                          'a-link-normal a-color-tertiary'})[-1].text

                print(detail_category)

                self.category_list.append(detail_category)

                self.processingCnt += 1

        print("카테고리 리스트 : {}".format(self.category_list))

        self.result['Detail Category'] = self.category_list

        print(self.result)

        return self.result

        self.browser.quit()

    def check_asin_count(self, asin):
        # 첫 번째 ASIN
        if self.processingCnt < 1:
            print("정상")
            self.browser.get(self.url.format(asin))
            time.sleep(1)
        else:
            print("프로세스 1 초과")
            self.browser.execute_script('window.open("{}");'.format(asin))
            self.browser.switch_to.window(self.browser.window_handles[self.processingCnt])

        return True





