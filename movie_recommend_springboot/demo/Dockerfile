# 클라우드 환경 설정 ubuntu 22.04
FROM ubuntu:22.04
#작업할 폴더 생성
WORKDIR /my_boot
#작업했던 파일들을 복사해서 my_boot에 복사
#COPY .(현재 폴더 DOCKER이 있는 폴더
#       /home/ubuntu/movie_recommend_flask)
#   .   (작업 폴더 /app)
COPY . .

####### 실행 환경 설정 명령 #######
RUN apt update

RUN apt install openjdk-11-jre-headless -y

RUN apt install maven -y

RUN mvn package -Dmaven.test.skip=true

# 사용할 포트 설정
EXPOSE 8080

# nohub로 실행 할 명령 설정
ENTRYPOINT [ "java", "-jar", "/my_boot/target/demo-0.0.1-SNAPSHOT.jar"]