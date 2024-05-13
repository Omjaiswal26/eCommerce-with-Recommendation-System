from django.urls import path
from .views import *

urlpatterns = [
    path('' , index , name='index'),
    path('anime' , anime , name='anime'),
    path('marvel' , marvel , name='marvel'),
    path('dc' , dc , name='dc'),
    path('search' , search , name='search'),
    path('about-us' , about_us , name='about_us'),
    path('privacy-policy' , privacy_policy , name='privacy_policy'),
    path('cancellation-policy' , cancellation_policy , name='cancellation_policy'),
    path('tnc' , tnc , name='tnc'),
]