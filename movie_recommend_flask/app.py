from flask import Flask,request
import json
import pymysql

import pandas as pd
import numpy as np
from tqdm.notebook import tqdm
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.preprocessing import StandardScaler

# 데이터베이스 연결
db = pymysql.connect(
            host = 'database-1.ccieoxitm8ik.ap-northeast-2.rds.amazonaws.com',
            port = 3306,
            user = 'admin',
            passwd='12341234', #aws 비밀번호
            db='movie_db',
            charset='utf8'
            )

# SQL 쿼리 문자열을 정의
sql = "SELECT * FROM movie_tbl"

# select 쿼리를 실행하고 결과를 movie_df에 저장
movie_df = pd.read_sql(sql, db)


# 모든행의 synopsys_vector 컬럼을 numpy 배열로 변환해서 synopsis_vector_numpy 컬럼에 대입
movie_df.loc[:,"synopsys_vector_numpy"] = movie_df.loc[:,"synopsys_vector"].apply(lambda x : np.fromstring(x, dtype="float32"))

#데이터의 각 열의 평균을 뺀 다음 표준편차로 나눠서 평균을 0로 표준편차를 1로 변환하는 StandardScaler 객체 생성
scaler = StandardScaler()

# 각 열의 평균 표준편차 계산
scaler.fit(np.array(movie_df["synopsys_vector_numpy"].tolist()))

# 데이터의 각 열의 평균을 뺀 다음 표쥰편차로 나눠서
# 평균을 0로 표준편차를 1로 변환 한 후
# 리스트로 변환해서 synopsys_vector_numpy_scale 컬럼에 대입
movie_df["synopsys_vector_numpy_scale"] = scaler.transform(np.array(movie_df["synopsys_vector_numpy"].tolist())).tolist()

# sysnopsys_vector_numpy_scale 컬럼의 유클리드 거리를 계산    
sim_score = euclidean_distances(
                movie_df['synopsys_vector_numpy_scale'].tolist(),
                movie_df['synopsys_vector_numpy_scale'].tolist()
            )

# sim_score (synopsys_vector_numpy_scale 컬럼의 유클리드 거리)DataFrame으로 변환
sim_df = pd.DataFrame(data=sim_score)

# sim_df의 인덱스에 영화 제목 대입
sim_df.index = movie_df["title"]

#sim_df의 컬럼명에 영화 제목 대입
sim_df.columns = movie_df["title"]

app = Flask(__name__)

# post 방식으로 movie_recommed URL일때 실행
@app.route('/movie_recommend', methods=["POST"])
def hello_world():
    #request.form["title"]: 입력한 제목을 리턴
    req_title = request.form["title"]
    #입력한 영화 제목과 가장 가까운 영화 3편을 result에 대입
    result = sim_df.sort_values(by=req_title)[1:4]
    #영화 제목이 저장된  result.index를 리스트로 변환
    result = result.index.to_list()
    
    #json.dumps :JSON 문자열로 변환
    result = json.dumps(result, ensure_ascii=False)
    # result 리턴
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0') #플라스크 시작 host='0.0.0.0'다른 컴퓨터에서 접속 가능