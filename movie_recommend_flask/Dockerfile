#운영체제 설정
FROM ubuntu:22.04
#작업할 폴더 생성
WORKDIR /app
#작업했던 파일들을 복사해서 my_boot에 복사
#COPY .(현재 폴더 DOCKER이 있는 폴더
#       /home/ubuntu/movie_recommend_flask)
#   .   (작업 폴더 /app)
COPY . .

# 리눅스 bash 쉘 (우리가 수업시간에 명렁어 입력했던 창)
#에서 명령어들이 실행되도록 설정
#도커는 기본으로 /bin/sh 창에서 명령들이 실행됨
SHELL [ "/bin/bash","-c" ]

#시스템 업데이트
RUN apt-get update
#파이썬 설치 -y : yes 자동입력
RUN apt-get install software-properties-common -y
#pip설치 -y : yes자동입력
RUN apt-get -y install python3-pip

#requirements.txt에 저장한 파이썬 라이브러리 설치
RUN pip install -r requirements.txt

#5000포트 사용 예정
EXPOSE 5000

#플라스크 실행
#외부 접속 가능 --host=0.0.0.0
#nohub로 실행 할 명령 실행(백그라운드로 항상 실행)
ENTRYPOINT [ "python3","-m","flask","run","--host=0.0.0.0"]