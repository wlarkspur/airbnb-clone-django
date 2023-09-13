import strawberry
import typing


"""
type annotaion " -> str: " 을 사용하면 strawberry가 알아서 처리해준다.
"""


@strawberry.type
class Query:
    pass


@strawberry.type
class Mutation:
    pass


# def 이하 return까지 graphql의 reseolver역할을 한다.
schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
)
