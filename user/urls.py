from django.urls import path

from user import apis

urlpatterns = [
    path('verify-phone', apis.verify_phone),
    path('login', apis.login),
    path('get-profile', apis.get_profile),
    path('set-profile', apis.set_profile),
]
