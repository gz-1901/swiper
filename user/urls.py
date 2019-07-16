from django.urls import path

from user import apis

urlpatterns = [
    path('verify-phone', apis.verify_phone),
]