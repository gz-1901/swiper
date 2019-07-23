from django.urls import path

from social import apis

urlpatterns = [
    path('recommend', apis.recommend),
    path('like', apis.like),
    path('dislike', apis.dislike),
    path('superlike', apis.superlike),
    path('rewind', apis.rewind),
    path('liked-me', apis.liked_me),
    path('top-rank', apis.top_rank),
]
