# -*- coding: utf-8 -*-
# @Time    : 10/31/19 6:18 PM
# @Author  : linix

import requests
import json
import re
from bs4 import BeautifulSoup
from urllib.parse import quote,unquote

headers = {
    'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Accept-Encoding': 'gzip,deflate,br',
    'Host': 'music.163.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
}

def getMusicLyric(songId, proxyIp=None):
    """
    :param songId: 网易音乐ID
    :param proxyIp: 代理，默认不使用代理
    :return: {'code':0,'songId':songId,'lyric':lyricText}
    """
    reqUrlPatt='https://music.163.com/api/song/lyric?id={songId}&lv=1&kv=1&tv=-1'
    reqUrl = reqUrlPatt.format(songId=songId)
    with requests.Session() as s:
        s.keep_alive = False
        if proxyIp:
            if isinstance(proxyIp,bytes):
                proxyIp=str(proxyIp,'utf-8')
            proxies = {
                'https': proxyIp
            }
            try:
                req = s.get(url=reqUrl, headers=headers, proxies=proxies, verify=False, allow_redirects=False,timeout=5)
            except BaseException as e:
                return {'code':-1,'songId':songId,'lyric':None}
        else:
            try:
                req = s.get(url=reqUrl, headers=headers, verify=False, allow_redirects=False, timeout=5)
            except BaseException as e:
                return {'code':-1,'songId':songId,'lyric':None}

    if req.status_code == 200:
        try:
            result = json.loads(req.text)
            code = result.get('code')
            noLyric=result.get('nolyric')
            if code == 200:
                if noLyric:
                    return {'code': 0, 'songId': songId, 'lyric': ''}
                else:
                    lyric = result.get('lrc', {}).get('lyric')
                    return {'code':0,'songId':songId,'lyric':lyric2Text(lyric)}
        except BaseException as e:
            print("解析网易音乐返回数据失败。reason:%s" % e)
    return {'code':-1,'songId':songId,'lyric':None}

def lyric2Text(lyric):
    """
    将歌词中音轨信息去除，返回纯文本
    """
    text=re.sub(r'\[[(\d)|:|\.]*\]','',lyric)
    return text.replace('-','').strip()

def getVideoRealUrl(videoId, proxyIp=None):
    """
    :param videoId: 网易视频ID
    :param proxyIp: 代理，默认不使用代理
    :return: {'code':0,'videoId':videoId,'url':realUrl}
    """
    reqUrlPatt=' https://music.163.com/video?id={videoId}'
    reqUrl = reqUrlPatt.format(videoId=videoId)
    with requests.Session() as s:
        s.keep_alive = False
        if proxyIp:
            if isinstance(proxyIp,bytes):
                proxyIp=str(proxyIp,'utf-8')
            proxies = {
                'https': proxyIp
            }
            try:
                req = s.get(url=reqUrl, headers=headers, proxies=proxies, verify=False, allow_redirects=False,timeout=5)
            except BaseException as e:
                return {'code':-1,'videoId':videoId,'url':None}
        else:
            try:
                req = s.get(url=reqUrl, headers=headers, verify=False, allow_redirects=False, timeout=5)
            except BaseException as e:
                return {'code':-1,'videoId':videoId,'url':None}

    if req.status_code == 200:
        bsobj=BeautifulSoup(req.text,'html.parser')
        try:
            url = bsobj.find('meta',attrs={'property':'og:video'}).attrs['content']
            if url:
                realUrl=unquote(unquote(url))
                return {'code': 0, 'videoId': videoId, 'url': realUrl}
        except BaseException as e:
            print("解析网易音乐返回数据失败。reason:%s" % e)
    return {'code':-1,'videoId':videoId,'url':None}

if __name__=='__main__':
    data=getVideoRealUrl('4127B34FE99E6BC7C38E69FBC823E3F5','117.43.49.232:4217')
    print(data)
