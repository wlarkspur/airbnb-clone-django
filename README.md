#Airbnb Django + Python ///////Comeback

poetry init: poetry 시작
poetry add django

poetry shell: shell 활성화를 위한 명령
django-admin startproject config .
django-admin
exit
#start project

poetry shell
python manage.py runserver
python manage.py migrate
python manage.py createsuperuser -> admin 계정생성
python manage.py startapp AAA #Model 내용 수정후 DB에 그사실을 알려줘야 한다. // 아래 2단계 매우 중요!
python manage.py makemigrations (migration 생성)
python manage.py migrate (migrate)
Application: 데이터와 데이터의 로직이 있는 섬같은 개념. models.py 어플리케이션에 있는 데이터의 정의나 
설명을 적는 곳. Django는 SQL데이터베이스 언어를 사용한다.(코드를 SQL로 자동 해석해준다.) models생성 
후에는 admin.py로 가서 생성한 model을 등록시켜야 한다.

django-admin startproject config .