# [코드&설명]
# !pip install pandas
# !pip install webdriver_manager
# !pip install PyMySQL
# !pip install selenium
# !pip install openpyxl
# !pip install wget

import wget
#2023년 박스 오피스 영화 리스트 url
url = "https://drive.google.com/uc?id=16MAmf6sFrs-tgGL4-dETRi_i7_hbObtU"
#파일 다운로드
wget.download(url)
from selenium import webdriver
from bs4 import BeautifulSoup
# from [selenium.webdriver.common.by](http://selenium.webdriver.common.by/) import By
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pymysql
import time
import pandas as pd

#최신 영화 박스 리스트
movie_2023 = pd.read_excel('box_office_2023.xlsx')
movie_2023
#결측치가 있는 행 삭제
movie_2023.dropna(axis=0, inplace=True)
movie_2023
#영화명 조회 (Series 타입)
movie_2023["영화명"]
#영화명을 리스트로 변환
movie_2023["영화명"].tolist()
#영화명을 리스트로 변환해서 movie_name_list에 대입
movie_name_list = movie_2023["영화명"].tolist()
movie_name_list

#데이터베이스 연결
db = pymysql.connect(
host='[database-1.ap-northeast-2.rds.amazonaws.com](http://database-1.ap-northeast-2.rds.amazonaws.com/)', #AWS Mysql Endpoint
port=3306,
user='admin',
passwd='passwd1234', #AWS Mysql password
db='movie_db',
charset='utf8'
)

#데이터베이스 쿼리를 실행할 객체 생성
cursor = db.cursor()
#크롬 드라이버의 옵션을 설정 할 객체
chrome_options = Options()
#브라우저 꺼짐 방지
chrome_options.add_experimental_option("detach", True)

#크롬 드라이버에 옵션 설정
driver = webdriver.Chrome(options=chrome_options)
#네이버 영화 검색 사이트 url
url = '[https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=영화](https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EC%98%81%ED%99%94)'
#페이지 로딩 될때 까지 최대 10초 대기 설정
driver.implicitly_wait(10)
#네이버 영화 검색 페이지 실행
driver.get(url)
#1초 대기
time.sleep(1)
for movie in movie_name_list:
    print("=" * 100)
    print("movie=",movie)
    print("=" * 100)
    #id 속성이 nx_query 인 객체를 search_box에 대입
    # search_box = driver.find_element([By.ID](http://by.id/), 'nx_query')
    search_box = driver.find_element(By.ID, 'nx_query')
    #기존에 입력한 메시지 삭제
    search_box.clear()
    #1초 대기
    time.sleep(1)
    #id 속성이 nx_query인 객체에 영화 영화 제목 입력
    search_box.send_keys('영화 ', movie)
    #클래스 속성이 bt_search인 객체 리턴
    search_button = driver.find_element(By.CLASS_NAME,'bt_search')
    #버튼 클릭
    search_button.click()
    #1초 대기
    time.sleep(1)
    try:
        #클래스 속성이 tab_list인 객체 리턴
        tab_list = driver.find_element(By.CLASS_NAME, 'tab_list')
        #클래스 속성이 tab _tab (클래스 속성이 tab _tab 2개 적용)  인 객체들 (여러개) 중 인덱스 1인 객체 리턴
        tab = tab_list.find_elements(By.CSS_SELECTOR,".tab._tab")[1]
        #탭 클릭
        tab.click()
        #1초 대기
        time.sleep(1)

        #페이지 소스 리턴
        html = driver.page_source
        #페이지의 정보를 추출 할 soup 객체 생성
        soup = BeautifulSoup(html, 'html.parser')
        #클래스 속성이 area_text_title인 객체의 문자열 리턴
        title = soup.select_one(".area_text_title").text
        print("title=",title)

        #클래스 속성이 detail_info인 객체 리턴
        detail_info = soup.select_one(".detail_info")
        #클래스 속성이 detail_info인 객체에 포함된 객체 중 클래스 속성이 _img인 객체 리턴
        img = detail_info.select_one("._img")
        #src 속성의 값 (영화 포스터의 url) 리턴
        poster = img['src']
        #영화 포스터의 url 출력
        print("poster=",poster)

        #클래스 속성이 info txt_4 (2개 클래스 적용) 인 객체 리턴
        info_group = soup.select_one(".info.txt_4")
        #dd 엘레먼트 리턴 (여러개)
        dd_list = info_group.select("dd")
        #0번째 dd의 문자열 리턴 (개봉일)
        open_date = dd_list[0].text
        print("open_date=",open_date)

        #1번째 dd의 문자열 리턴 (등급)
        degree = dd_list[1].text
        print("degree=",degree)

        #2번째 dd의 문자열 리턴 (장르)
        genre = dd_list[2].text
        print("genre=",genre)

        #3번째 dd의 문자열 리턴 (국가)
        country = dd_list[3].text
        print("country=",country)

        #4번째 dd의 문자열 리턴 (상영시간)
        movie_time = dd_list[4].text
        print("movie_time=",movie_time)

        #5번째 dd의 문자열 리턴 (회사)
        company = dd_list[5].text
        print("company=",company)

        #클래스 속성이 text _content_text (2개 클래스 적용) 인 객체 문자열 리턴
        synopsis = soup.select_one(".text._content_text").text
        print("synopsis=",synopsis)

        #movie_tbl 테이블에 영화 정보를 저장할 SQL 쿼리 생성
        sql = 'insert into movie_tbl (title,poster,degree,genre,open_date,country,movie_time,synopsys) '
        sql += '              values (%s,    %s ,   %s,    %s,     %s,         %s,     %s,         %s)'

        #sql 쿼리 실행 (%s에 변수의 값 대입)
        cursor.execute(sql,(title,poster,degree,genre,open_date,country,movie_time,synopsis))
        #커밋 실행(데이터베이스에 데이터 저장)
        db.commit()
    except Exception as e:
        print("수집하고자 하는 데이터 중 없는 데이터 (주로 줄거리) 가 있어서 에러가 발생 함")

