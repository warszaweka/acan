from acan.schema import Query as AcanQuery
from graphene import ObjectType, Schema


class Query(AcanQuery, ObjectType):
    pass


schema = Schema(query=Query)
