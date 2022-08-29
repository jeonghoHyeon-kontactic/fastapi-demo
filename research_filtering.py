import os
import glob
import pandas as pd


class ResearchFiltering:

    download_directory = 'C:/Users/user/Downloads/'

    def __init__(self):
        print("CSV 파일 필터링")
        self.asins = []
        self.result = pd.DataFrame()
        self.num = 1

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

        return dfresult