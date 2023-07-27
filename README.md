# machine learning start
git : 파이참 clone-> 
setting메뉴 선택후 project:machine learning 클릭 
add interpreter 
클릭후 가상환경 구축 
-> 터미널에서 가상환경 진입후 
패키지 설치 진행 
패키지 설치 : pip install -r requirements.txt 
패키지 업로드 : pip freeze > requirements.txt
# celery 작업정보 보기
celery -A core worker -l info
window에서 필요한 패키지 
pip install gevent
우분투에서는 필요없다.
celery -A core worker -l INFO #실행키 

# RabbitMQ 설치.
https://heodolf.tistory.com/50

celery -A core worker -l info -P gevent

https://heodolf.tistory.com/54