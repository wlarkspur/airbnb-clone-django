from django.db import models

""" 아래 모델은 데이터베이스에 들어가지 않고 다른 APP들이 사용할 수 있게 된다.
    
    class Meta:
        abstract = True 

    abstract는 model이 DB에서 실제 데이터로 사용되지 않게 된다.
    아래 코드는 재사용하기 위한 코드이다.
"""


class CommonModel(models.Model):

    """Common Model Definition"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
