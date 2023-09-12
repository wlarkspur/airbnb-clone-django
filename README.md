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
22. App 내부의 views.py는 꼭 views로 이름을 해야되는건 아니다. config의 url.py에서 views 파일을 모두 import해서 사용하기 때문이다.
    그 외 models.py, apps.py. admin.py 는 무조건 이 이름을 사용해야 한다.
    그럼에도 views.py를 그대로 사용하는게 관례이므로 굳이 바꿔서 쓰지 않도록 한다.
23. request object는 요청하고 있는 브라우저의 정보, 전송하고 있는 데이터, 요청한 url 정보, ip 주소, 쿠키 등을 모두 가지고 있다.
24. url.py 의 path의 첫 번쨰 arg는 유저가 이동할 url이고 두 번째 arg는 유저가 해당 url로 왔을때 장고가 실행할 함수이다.

Divdie and Conquer 

25. 각 어플리케이션은 urls.py를 가지게 하고 config.urls.py는 모든 url을 통합하는 역할을 시킨다.
26. Backend에서는 django를 쓰고 Frontend에서는 React를 쓰는게 표준이 되었다. 2023Y
27. serializer 는 django python 객체를 JSON으로 번역하는 역할을 한다.
    반대로 유저에게서 JSON 데이터를 받아 DB에 적용할 수 있는 Django 객체로 바꿔주기도 한다.
28. DB에서 넘어오는 Django 객체를 번역하려면 
    CategorySerializer의 모델에 instance인 category를 첫 argument(인자)로 넘겨주면 된다.
    ex: serializer = CategorySerializer(category)
    반대로 user가 보낸 데이터를 serializer로 넘기고 싶다면 아래와 같이 코드를 작성한다.
    ex: serializer = CategorySerializer(data=request.data)
    *seriallizer.is_valid()를 통해 데이터 값이 유효한지 확인할 수도 있다.
        유효성 검사는사용자가 정의한 모델의 제약조건, Serializer 클래스의 유효성 검사 규칙을 기반으로 수행 된다.
    pk = serializers.IntegerField(read_only=True) 
    위 코드의 read_only=True는 데이터의 직렬화(serialization)할때는 필드 값을 표현하거나, 반환할 수 있지만, 역직렬화 할때는 해당 필드를 업데이트하는 것이 불가능해 진다.

```python
serializer = CategorySerializer(
    category,
    data=request.data,
    partial=True,
    )
```
위 코드에서 partial=True는 부분 업데이트를 허용하고, 요청에 포함된 데이터만을 업데이트하는데 사용된다.

29. save() / serializer.save()를 실행하면 자동으로 create 객체를 검색한다.
    우리가 할일은 create 객체 생성을 하는 것이다. // Chanllenging...
30. raise 가 실행되면 그 뒤의 코드는 실행되지 않는다..
31. api 마다 version을 표기하도록하자.
32. serializer 는 번역기로 어떤 기기종류든 핸드폰, 브라우저 누구에게나 데이터를 줄수 있는 json 모델로 번역을 해준다. Django rest_framework는 serializer를 만들수 있도록 도와준다.
    *만약 사용자 데이터 만으로 serialzer를 만들었고 serializer.save()를 한다면 create 메소드가 실행된다.(Django는 사용자 데이터로 무언가를 생성하려는 것을 알게 된다.)
    *만약 데이터베이스(DB)의 데이터와 사용자 데이터로 serializer를 만드려하면 데이터 업데이트하려는 것을 알고 update 메소드가 호출 된다.......
33.  

```python
class CategorySerializer(serializers.ModelSerializer)
class Meta:
    model = Cateogry
    fields = "__all__"
```
위와같이 serializers.ModelSerializer 를 사용하여 Serializer와 Model을 자동으로 연결시켜줄 수 있다.
34. viewsets ModelViewSet
```python
class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
```
이 3줄의 코드로 viewSet을 대신할 수 있다.

**Trade-offs(장단점):
    viewSet은 코드 수를 줄여주고, 다른 일에 더 신경을 쓸 수 있도록 도와주지만
    view처럼 직접 작성된 코드보다는 명확성이 떨어지게 된다. 
    예를들어 커스텀 코드 작성시 viewSet안에서 한계가 생기게 된다.
    explicit is better than implicit

35. APIView를 사용하면 request method가 GET인지 POST인지 확인하는 조건문 코드를 쓰지 않아도 된다.
36. 
    1. application의 urls.py는 config의 urls과 연결되어 있다.
    2. serializers.py는 class Meta: 를 이용하여 만든 Class를 통해서 model과 serializer는 연결시켜주는데 rest_framwork.serializers import ModelSerializer 를 활용한다. 
    3. views는 앞서 만든 model, serialzier를 활용하여 APIView를 통해 api화면을 세팅할 수있도록 해준다.
37. 

```python
class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"
        depth = 1
```
depth는 API하위 관계트리를 모두 확장시켜주는데, 커스터 마이징이 불가능하다.
depth는 아주 간단하고 빠르게 모델의 모든 관계를 확장시키는데 유용하다.
모든 관계를 확장시키기 때문에 불필요한 정보까지 노출될 수 있는데, 이를 위해서 model의 관계를 어떻게 커스터마이징 할 수 있을지 알아야 한다.

```python
class RoomDetailSerializer(ModelSerializer):
    owner = TinyUserSerializer()
    amenities = AmenitySerializer(many=True)

    class Meta:
        model = Room
        fields = "__all__"

```

위 코드는 owner, amenities의 커스터마이징 코드이다. many=True설정을 해줘야만 여러개의 관계 api를 불러오게 된다.
many=True는 List, Array가 아니고 단지 숫자만 있다면 해당 설정을 하지 않아도 된다.
만약 사용하면 "object is not iterable"이란 오류를 뿜어내므로 참고.

38. 29->recap
user 데이터만으로 save()를 실행하면 자동으로 create method를 호출하게 된다.
create(),save() Method의 validated_data에 추가로 데이터를 추가하고 싶다면
save를 호출할때 호출할 데이터를 추가해주는 것이다.

example:
```python

if serializer.is_valid():
                room = serializer.save(owner=request.user)
                serializer = RoomDetailSerializer(room)
                return Response(serializer.data)

```
39. APT ManyToMany 의 경우 snippet.add(@) 의 방식으로 ["add"]를 통해 추가해줘야한다.
40. transaction
```python
with transaction.atomic():
```
with 다음에 오는 코드 중에 error가 한개라도 발생하면 DB에 반영하지 않게 한다.
transaction 하위코드에는 try-except를 사용하지 않도록 해야, error가 발생한 것을 인지하고 제대로 동작할 수 있다.
ex: 비행기 티켓구매 사이트를 만든다 가정하면, 왕복 티켓을 모두 구입하게 만들어야 하는데 편도로 작성되면 DB에 반영하지 않게 하는 것을 예로 들 수 있다.

41. serialzier 에서 method 호출방법.

```python
rating = serializers.SerializerMethodField()
```
위 코드와 같이 serializers.SerializerMethodField()를 사용하면 
```python
def get_rating(self, room):
        return room.rating()
```
위와 같이 get_ 에 rating을 추가하여 models에 있는 method를 serializer로 호출하여 사용할 수 있게되면서, 필드에 새로운 변수를 추가할 수 있다.

42. room하나는 수만 개의 리뷰를 가질 수 있기 때문에 해당 방을 보여줄 때, reverse accessor(역접근자) 를 포함하는 건 좋은 아이디어가 아니다. 잘못하면 DB를 다운 시킬수도 있다. 만약 리뷰가 10만개라면 단 하나의 Query로 인해 DB가 셧다운 될 수있다. 이를 방지하기 위해 pagination기능이 필요하다. 
43. Pagination
pagination을 위해서 제일 먼저 할것은 페이지를 만드는 것이다 (?)
```python
page = request.query_params.get("page", 1)
```
위 처럼 get("page", 1)의 숫자 1은 default 값으로 페이지가 없다면 1페이지를 기본값으로 가지게 된다.
```python
page_size = 3
        start = (page - 1) * page_size
        end = start + page_size
```
- page_size: 이는 offset에 해당하는 값으로 한 페이지에 보여지는 콘텐츠 개수이다
- start에서 -1 즉 1페이지 -1로 0을 유도하여 index 0 부터 end 값 start + page_size를 더해줌으로써 0, 1 ,2 총 3개의 콘텐츠를 보여주게 할 수 있다.
수식 1 * page_size 는 페이지가 1개씩 증가함에 따라 page_size의 배수로 증가한다.
end에서는 위에서 계산된 start 에 단순히 page_size를 더함으로써 각 배수마다 보여지는 콘텐츠의 수를 영리하게 추가해주고 있다.
```python
serializer = AmenitySerializer(
            room.amenities.all()[start:end],
            many=True,
        )
```
위 코드는 Django가 제공하는 페이지네이션 도움 코드로, 배열[0:3]을 제시하면 index 0~2까지의 값을 보여주도록 API를 구성해준다.

44. config.settings.py 에 생성하는 MEDIA_ROOT = "" 은 업로드 저장할 폴더를 물어보게 된다.
```python
MEDIA_ROOT = "uploads"
```
이렇게하면 root 경로에 uploads 폴더안으로 사진을 저장하게 된다. 
이때 uploads앞에 / 를 사용할 필요없다. 
MEDIA_ROOT: 파일이 실제 있는 폴더
MEDIA_URL: 파일을 노출하는 방법

**주의 이 방법은 개발단계에서만 사용해야 되며, 실제 배포에는 보안상 심각한 위험을 가지고 있으므로 파일 저장은 Cloud 서버를 이용해야 한다. 만약 그대로 배포하면 User는 아무런 파일을 우리 서버 코드옆에 바로 업로드 시킬수 있다는 의미이다. 미친짓이다.

45. permission_classes = [IsAuthenticatedOrReadOnly]
Model 객체 안에 위 코드를 사용하게 되면, 누구나 접근가능하게 하지만 인증된 사람만 편집권한을 가지게 된다.

```python
def put(self, request, pk, room_pk):
        wishlist = self.get_list(pk, request.user)
        room = self.get_room(room_pk)
        if wishlist.rooms.filter(pk=room.pk).exists():
            # .exists()가 있으면 TRUE,FALSE 값을 받고, 아니면 list값을 받는다.
            wishlist.rooms.remove(room)
        else:
            wishlist.rooms.add(room)
        return Response(status=HTTP_200_OK)
```
위 코드에서 pk, rooom_pk는 url 경로에서 전달되는 값으로 urls.py에 지정한 값과 동일해야 한다.
46. 
```python
from django.utils import timezone
```
Django timezone은 config.settings의 timezone을 알려주고 사용한다.
*timezone.now() 는 UTC 기준 시간대를 가져온다.
*timezone.localtime()은 서버기준 시간대를 가져온다.
이러한 차이로 전세계 동시 접속하는 사람들간의 서로 다른시간대를 고려하면 UTC기준의 시간을 가져와 각자 로컬시간대로 아래와 같이 사용하는것이 적절하다.
```python
timezone.localtime(timezone.now())
# timezone.now()에서 UTC시간을 받은 뒤 localtime으로 변경해준다.
```
47. serializer validate를 활용해서 아래와 같이 입력데이터를 검증할 수 있다.
```python 
    def validate_check_in(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        return value

    def validate_check_out(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now >= value:
            raise serializers.ValidationError("Can't book(check_out) in the past!")
        return value
```
아래와 같이 check_in__lte or gte = data["check_in"] 을 사용해 기존 예약날짜가 신규예약 날짜와 겹치지 않는지 확인할 수 있다.
```python
Booking.objects.filter(
            check_in__lte=data["check_out"],
            check_out__gte=data["check_in"],
        ).exists()
```
**validation은 serialzier 안에서 이루어지도록 하는것이 좋다.

추가: 
```python
        if serializer.is_valid():
            booking = serializer.save()
            serializer = PublicBookingSerializer(booking)
            return Response(serializer.data)
```         
해당 코드는 데이터 유효성 검사릍 통과후 저장하여 새로운 객체를 만든 후 다시 데이터를 serializer하여 이를 클라이언트로 응답을 보내는 과정이다.
48. ModelSerializer는 중복 값에 대한 유효성 검사를 알아서 해준다.
**비밀번호에 대해서는 사용자가 직접 유효성 검사를 진행해야 한다.
```python
user = serializer.save()
            user.set_password(password)
            user.save()
```
아래 코드는 Password를 바꾸기 위한 put 요청으로 만든 코드이다.
```python
 def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            raise ParseError
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
```
*check_password, set_password 기능이 있다는것을 염두에 두자.

49. 
```python
from django.contrib.auth import authenticate, login
```
 1. authenticate: username, password를 주는 function
    username, password가 맞으면 django는 user를 리턴한다.
 2. user를 로그인시켜주는 function으로 user, request를 보내주면 django는 브라우저가 필요한 쿠키와 token 등 중요한 정보를 준다.
 50. Code check challenge Done...

 51. strawberry GraphQL 라이브러리 예시
 **Strawberry**
 Strawberry는 GraphQL Schema를 Python 클래스로 정의하고 사용할 수 있게 해주는 라이브러리.
 아래 코드는 그 예시이며 간단히 설명하면
 movies는 typing도구를 이용해 Movie List를 반환하고 뒤에 strawberry.field는 
 resolver를 통해 field값을 어디서 가져올지 지정해주는 코드이다.
 *mutation*의 경우
 add_movie field는  strawberry.mutation 함수에 의해 정의되었다.
 GraphQL Schema에 add_mutation을 추가하는 역할을 한다.
 ```python
 @strawberry.type
class Query:
    movies: typing.List[Movie] = strawberry.field(resolver=movies)
    movie: Movie = strawberry.field(resolver=movie)

@strawberry.type
class Mutation:
    add_movie: Movie = strawberry.mutation(resolver=add_movie)
 ```