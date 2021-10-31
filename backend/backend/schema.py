from graphene import Schema

from acan.schema import Mutation, Query

schema = Schema(query=Query, mutation=Mutation)
