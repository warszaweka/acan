from django.contrib.admin import site
from django.urls import include, path
from graphene_django.views import GraphQLView

urlpatterns = [
    path('admin/', site.urls),
    path('graphql', GraphQLView.as_view()),
    path('acan/', include('acan.urls')),
]
