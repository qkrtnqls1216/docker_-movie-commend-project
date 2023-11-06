# [코드&설명]
# !pip install scikit-learn

import os
import pymysql
import time
import pandas as pd
import numpy as np
from tqdm.notebook import tqdm
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.preprocessing import StandardScaler
import json

# 데이터베이스 연결

db = pymysql.connect(
host = '[database-1.ccieoxitm8ik.ap-northeast-2.rds.amazonaws.com](http://database-1.ccieoxitm8ik.ap-northeast-2.rds.amazonaws.com/)',
port = 3306,
user = 'admin',
passwd='12341234',
db='movie_db',
charset='utf8'
)
sql = "select * from movie_tbl;"

movie_df = pd.read_sql(sql, db)
movie_df
string_array = movie_df.loc[0,"synopsys_vector"]
string_array
np.fromstring(string_array, dtype="float32")
numpy_array = np.fromstring(string_array, dtype="float32")
numpy_array
movie_df.loc[:,"synopsys_vector"]
movie_df.loc[:,"synopsys_vector"].apply(lambda x : np.fromstring(x, dtype="float32"))
movie_df.loc[:,"synopsys_vector_numpy"] = movie_df.loc[:,"synopsys_vector"].apply(lambda x : np.fromstring(x, dtype="float32"))
movie_df
movie_df["synopsys_vector_numpy"]
movie_df["synopsys_vector_numpy"].tolist()
np.array(movie_df["synopsys_vector_numpy"].tolist())
scaler = StandardScaler()
scaler.fit(np.array(movie_df["synopsys_vector_numpy"].tolist()))

# 각 열의 평균

scaler.mean_

# 각 열의 분산

scaler.var_
scaler.transform(np.array(movie_df["synopsys_vector_numpy"].tolist()))
scaler.transform(np.array(movie_df["synopsys_vector_numpy"].tolist())).tolist()
movie_df["synopsys_vector_numpy_scale"] = scaler.transform(np.array(movie_df["synopsys_vector_numpy"].tolist())).tolist()
movie_df
movie_df["synopsys_vector_numpy_scale"]
sim_score = euclidean_distances(movie_df["synopsys_vector_numpy_scale"].tolist(),movie_df["synopsys_vector_numpy_scale"].tolist())
sim_score
sim_score[0]
sim_df = pd.DataFrame(data=sim_score)
sim_df.index = movie_df["title"]
sim_df
sim_df.columns = movie_df["title"]
sim_df

# 오토라는 남자 영화의 거리가 가까운 순으로 조회

sim_df["오토라는 남자"].sort_values()
sim_df["오토라는 남자"].sort_values()[1:4]
pd.DataFrame(sim_df["오토라는 남자"].sort_values()[1:4])
pd.DataFrame(sim_df["오토라는 남자"].sort_values()[1:4]).reset_index()
pd.DataFrame(sim_df["오토라는 남자"].sort_values()[1:4]).reset_index().values
pd.DataFrame(sim_df["오토라는 남자"].sort_values()[1:4]).reset_index().values.tolist()
result = pd.DataFrame(sim_df["오토라는 남자"].sort_values()[1:4]).reset_index().values.tolist()
json.dumps(result, ensure_ascii=False)