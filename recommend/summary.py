# [설명&코드]

# 영화 줄거리 벡터 변환

# !pip install konlpy
# !pip install pandas
# !pip install PyMySQL

# 한국어 전처리를 위한 Twitter 설치

# !pip install Twitter
# !pip install tqdm
# !pip install gensim
# !pip install --upgrade jupyter ipywidgets

import os
import pymysql
import time
import pandas as pd
import numpy as np
from tqdm.notebook import tqdm
from gensim.models.word2vec import Word2Vec

# 자바 경로 설정
os.environ["JAVA_HOME"] = "C:\Program Files\Java\jdk-11"

# 한국어 형태소 분석기 Twitter
from konlpy.tag import Twitter
twitter = Twitter()

# 텍스트 전처리 함수
def preprocessingText(text):
    stems = []
    tagged_review = twitter.pos(text, stem=True)
    for word, pos in tagged_review:
        if pos == "Noun" or pos == 'Adjective':
            stems.append(word)
    return " ".join(stems)

# 데이터베이스 연결
db = pymysql.connect(
    host='[database-1.ccieoxitm8ik.ap-northeast-2.rds.amazonaws.com](http://database-1.ccieoxitm8ik.ap-northeast-2.rds.amazonaws.com/)',
    port=3306,
    user='admin',
    passwd='12341234',
    db='movie_db',
    charset='utf8'
)

# 영화 정보 쿼리
sql = "select * from movie_tbl;"

# 영화 정보 데이터프레임으로 로드
movie_df = pd.read_sql(sql, db)

# 줄거리 전처리를 위한 새로운 열 생성
movie_df['synopsys_clear'] = np.NaN

# 더미 반복 작업 (임시)
sum = 0
for i in tqdm(range(10000000)):
    sum = sum + i

# 영화 정보 데이터프레임의 행 수
row_num = len(movie_df)

# 각 행에 대한 줄거리 전처리 수행
for index in tqdm(range(row_num)):
    try:
        synopsys = movie_df.loc[index, "synopsys"]
        movie_df.loc[index, "synopsys_clear"] = preprocessingText(synopsys)
    except Exception as e:
        movie_df.loc[index, "synopsys_clear"] = np.NaN

# 더미 데이터 생성
movie_df["synopsys_clear"] = movie_df['synopsys_clear'].astype(str) + " "

# 더미 데이터를 공백을 기준으로 리스트로 변환
movie_df["synopsys_clear_list"] = movie_df["synopsys_clear"].apply(lambda data: data.split(" "))

# Word2Vec 모델 생성
word2vec = Word2Vec(movie_df["synopsys_clear_list"], sg=1, vector_size=80, window=3, min_count=2, workers=10)

# Word2Vec 모델의 단어 목록
word2vec_words = word2vec.wv.key_to_index.keys()

# 영화 정보 조회 및 Word2Vec 벡터 생성
for index in range(3):
    num = movie_df.loc[index, "num"]
    print("num=", num)
    title =  movie_df.loc[index, "title"]
    print("title=", title)
    line = movie_df.loc[index, "synopsys_clear_list"]
    print("line=", line)
    doc2vec = None
    count = 0

    for word in line:
        print("word=", word, end="\t")
        if word in word2vec_words:
            count += 1
            if doc2vec is None:
                doc2vec = word2vec.wv[word]
            else:
                doc2vec = doc2vec + word2vec.wv[word]

    if doc2vec is not None:
        doc2vec = doc2vec / count

    print()
    print("="*100)
    print("num=", num, "title=", title, ":doc2vec=", doc2vec)
    print("="*100)

# 데이터베이스 연결 닫음
db.close()