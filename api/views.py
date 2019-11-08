# -*- coding: utf-8 -*-
# @Time    : 5/7/19 1:30 AM
# @Author  : linix

from rest_framework import generics,permissions,viewsets,status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from django.http import Http404
import redis
import random

from .utils.NeteaseMusicApis import getMusicLyric,getVideoRealUrl


domainZSetKey='PROXYPOOL:DOMAINS'
domainsProxyZSetKey='%(domain)s:ProxySortedSet'
proxyServer=redis.Redis(host=settings.PROXY_REDIS['HOST'], port=settings.PROXY_REDIS['PORT'],db=settings.PROXY_REDIS['DB'],password=settings.PROXY_REDIS['PASSWORD'])

class ApisListView(APIView):

    def get(self, request, format=None):
        introduction={
            'api/music/netease/lyric/<songId>':'网易歌曲歌词',
            'api/music/netease/videoUrl/<videoId>': '网易视频源地址（短期）',
        }
        return Response(introduction)

class MusicNeteaseLyricView(APIView):

    def get(self, request,pk, format=None):
        proxyServer.zadd(domainZSetKey,{'163.COM':16})
        proxyList=proxyServer.zrange(domainsProxyZSetKey % {'domain': '163.COM'},0,-1)
        proxy=random.choice(proxyList)
        data=getMusicLyric(songId=pk,proxyIp=proxy)
        if data.get('code')==-1:
            return Response(data,status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(data)

class MusicNeteaseVideoUrlView(APIView):

    def get(self, request,pk, format=None):
        proxyServer.zadd(domainZSetKey,{'163.COM':16})
        proxyList=proxyServer.zrange(domainsProxyZSetKey % {'domain': '163.COM'},0,-1)
        proxy=random.choice(proxyList)
        data=getVideoRealUrl(videoId=pk,proxyIp=proxy)
        if data.get('code')==-1:
            return Response(data,status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(data)