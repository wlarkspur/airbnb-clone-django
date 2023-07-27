#Airbnb Django + Python //////// 22.novoselie

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

1. Django에서는 ID 대신 PK(Primary Key)를 사용한다.
2. on_delete = models.SET_NULL 값은 사용자가 계정을 삭제해도 그의 기록을 유지하고 싶을 때 사용한다. 
    결제 내역같은 정보가 이에 해당한다.
3. models.ImageField()를 사용하기 위해선 poetry add Pillow 명령어로 설치해준다.
4. python manage.py startapp common: common은 App들이 공용으로 사용할 수 있는 코드를 가진 앱.
5. App을 설치한 후에는 config.setting에서 app을 설치해준다.
6. blank=True는 Django Forms에서 비어있는 칸을 허용하고
    null=True는 DB에서 null 값을 허용한다.
7. def __str__(self) -> str:
        return f"{self.kind.title()}: {self.name}" 
    정의를 통해서 models에서 정해진 kind의 title 대문자로 바꿔준다.
8. models.OneToOneField()는 Unique 값을 의미한다. 모델간의 연결을 고유하게 만든다.
   ex: 유저의 결제 정보를 저장할때 사용할 수 있다.
9. 어플리케이션 에서 같은 모델 명을 가진것은 문제가 되지 않지만, 2개의 모델이 같은 모델(USER)과 연결이 되어있다면 문제가 된다.
10. ORM (Object-relational mapping): 객체와 관계형 DB의 data를 자동으로 매핑해주는 것을 말함.
11. python manage.py shell : InteractiveConsel
12. model.objects.get(): 단 하나의 값만 찾는다.
    model.objects.all(): 모든 값을 검색
     *만약 model값이 100million개 있다면 DB가 부담이 될 것 같지만, Lazy하게 검색하므로, 직접 요청한 데이터만 가져오게 된다.
    model.objects.filter(price__lte=1500): price가 1500이하 인값을 검색
    model.objects.filter(name__contains="gangnam"): name에 "gangnam"이 포함된 값 검색
    model.objects.filter(name__startswith="Apart"): name에 "Apart"로 시작하는 값 검색
    models.objects.create(): 새로운 값 생성
    models.objects.delete(): 값 삭제 / Manager객체에는 'delete'메서드가 없으므로, 
    다음과 같이 삭제한다.
    amenity_instance = Amenity.objects.get(pk=7)
    amenity_instance.delete()
    한줄로 삭제하려면 
    model.objects.filter(pk=7).delete()
    delete()를 호출하면 해당 쿼리셋에 포함된 모든 레코드가 삭제되므로 주의.
13. QuerySet은 Lazy하기 때문에 DB를 힘들게 하지 않고 데이터를 가져올 수 있다.(ex: .exclude(),   count())
14. reverse는 특정 값을 가리키는 model을 찾기 위함이다.
    models.objects.filter(owner__username="AAA")를 통해 models의 owner의 username="AAA"가 가진 값들을 검색할 수 있게된다.
    ** __ 는 매직코드 같다.
    ex/ Room.objects.filter(owner__username='som') username som이 가진 Room 검색.
        Room.objects.filter(owner__username__startswith='so') 더블 __(밑줄*2)를 사용가능.
15. review_set, room_set 를 dir(User)가 가지고 있다면, review는 user는 Forign_Key를 가리키고 있다는 의미이다. review는 user를 가리키고, room도 user를 가리킬때 dir(User)에서 review_set, room_set이 나타나게 된다.       
16. reverse accessors(역접근자): model A가 model B에 Foreign Key,ManyToMany 등...을 가질때, 
    자동적으로 모델 B는 'Model A_set'을 가지게 된다. 이를 커스터마이징 가능하다.
    ex/ model A의 Foreign Key 값에 'related_name=' 을 통해 커스터마이징하면 
    모델 B는 'Model A_set'대신 related_name값을 가지게 된다.
17. 사소한 최적화 방법: 
    1. room.reviews.all().values("rating"):
        room 의 reviews(review_set)의 모든 값에서 rating 딕셔너리 값을 받아온다.
    2. room.reviews.all()
        room 의 reviews의 모든 값을 가져온다.
    1번의 경우 약간의 최적화를 거친 코드이며, 2번은 DB가 많을 경우 작업속도를 지연시킬 수 있다.
    extra: room.reviews 이후 부터는 manage 작업인 filter, get등 여러가지 사용가능하다.
18. search_fields 값 설정법:
        "^name" : startswith와 같다.
        "=name" : 정확히 일치하는 값을 찾는다.
19. Admin action에는 3개의 매개변수가 필요하다.
    1. 이 액션을 호출한 클래스인 model_admin
    2. 이 액션을 호출한 유저 정보를 가지고 있는 request객체
    3. QuerySet 뭐라고 이름짓든 상관없다.
    관리자 페이지를 구축하거나, 동시에 여러 값들을 리셋하거나 수정할 때 액션을 사용할 수 있다.
    엑셀에 데이터를 보내거나 owner를 바꾸거나 데이터 변경을 하고 싶을때 도움을 준다.
    실무에서도 활용도가 높다.
20. lookups는 튜플 list를 리턴하는 함수로
    첫번쨰 요소는 url에 나타나고
    두번째 요소는 유저가 클릭하게 되는 텍스트고
    세번째는 queryset으로 필터링 된 객체, 즉 린턴해야한느 메소드다.
21. queryset 의 self.value()가 url에 보이는 word를 주게 된다.
    필터링 작업 없이도 리턴핫 수 있도록 해야한다.(필터 "모두, All" 옵션 선택시)

