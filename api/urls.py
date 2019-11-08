# -*- coding: utf-8 -*-
# @Time    : 5/7/19 1:33 AM
# @Author  : linix

from django.urls import path,include
from rest_framework import routers
from . import views

app_name='api'

router=routers.DefaultRouter()

urlpatterns=[
    path('', include(router.urls)),
    path('introduction/',views.ApisListView.as_view(),name='introduction'),
    path('music/netease/lyric/<pk>/', views.MusicNeteaseLyricView.as_view(), name='music_netease_lyric'),
    path('music/netease/videoUrl/<pk>/', views.MusicNeteaseVideoUrlView.as_view(), name='music_netease_videoUrl'),
]