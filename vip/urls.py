from django.urls import path

from vip import apis

urlpatterns = [
    path('info', apis.info),
]