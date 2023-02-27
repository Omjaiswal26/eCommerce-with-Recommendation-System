from django.urls import path
from .views import *

urlpatterns = [
    path('' , index , name='index'),
    path('anime' , anime , name='anime'),
    path('marvel' , marvel , name='marvel'),
    path('dc' , dc , name='dc'),
    path('search' , search , name='search'),
]