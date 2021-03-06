import sys
from mirai import Mirai, Plain, MessageChain, Friend, Face, MessageChain, Group, Image, Member, At
from mirai.face import QQFaces
from bs4 import BeautifulSoup
from PIL import ImageFont, ImageDraw
from PIL import Image as PImage
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import asyncio
import requests
import json5
import json
import numpy
import random
import os
import base64
import qrcode
import io
import string
import math
import copy
import ctypes
import functools
import traceback
import http.client
import statistics
import csv
import hashlib
import zlib
import time
import datetime
import urllib
import mido
import GLOBAL
from Utils import *
sys.dont_write_bytecode = True

res = ''
try:
    with open('cfg.json', 'r') as jfr:
        cfg = json.load(jfr)
        proxy = cfg.get('proxy', {})
        appid = cfg.get('appid', '')
        secretKey = cfg.get('secretKey', '')

except Exception as e:
    proxy = {}
    appid = ''
    secretKey = ''


def BDtranslate(req):
    trans = None
    myurl = '/api/trans/vip/translate'
    fromLang = req[0]
    toLang = req[1]
    salt = random.randint(32768, 65536)
    q = req[2]
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
        q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign

    try:
        trans = http.client.HTTPConnection('api.fanyi.baidu.com')
        trans.request('GET', myurl)
        response = trans.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)
        res = result['trans_result'][0]['dst']

    except Exception as e:
        res = e

    finally:
        if trans:
            trans.close()
    return res

# 好好说话


def hhsh(req):
    result = ''
    url = 'https://lab.magiconch.com/api/nbnhhsh/guess'
    head = {'Content-Type': 'application/json'}
    re = {'text': req}
    res = json.loads(requests.post(
        url, headers=head, json=re, timeout=30).text)
    try:
        for i in res[0]['trans']:
            result += '\n'+i
    except:
        result = '\n尚未收录'
    return result

# 无符号位移: https://www.jianshu.com/p/24d11ab44ae6
# 这个函数可以得到32位int溢出结果，因为python的int一旦超过宽度就会自动转为long，永远不会溢出，有的结果却需要溢出的int作为参数继续参与运算


def int_overflow(val):
    maxint = 2147483647
    if not -maxint-1 <= val <= maxint:
        val = (val + (maxint + 1)) % (2 * (maxint + 1)) - maxint - 1
    return val


def unsigned_right_shitf(n, i):
    # 数字小于0，则转为32位无符号uint
    if n < 0:
        n = ctypes.c_uint32(n).value
    # 正常位移位数是为正数，但是为了兼容js之类的，负数就右移变成左移好了
    if i < 0:
        return -int_overflow(n << abs(i))
    return int_overflow(n >> i)


def google_TL(src):
    a = src.strip()
    b = 406644
    b1 = 3293161072

    jd = "."
    美元b = "+-a^+6"
    Zb = "+-3^+b+-f"

    e = []
    for g in range(len(a)):
        m = ord(a[g])
        if 128 > m:
            e.append(m)
        else:
            if 2048 > m:
                e.append(m >> 6 | 192)
            else:
                if 55296 == (m & 64512) and g + 1 < len(a) and 56320 == (a[g+1] & 64512):
                    g += 1
                    m = 65535 + ((m & 1024) << 10) + (a[g] & 1023)
                    e.append(m >> 18 | 240)
                    e.append(m >> 12 & 63 | 128)
                else:
                    e.append(m >> 12 | 224)
                    e.append(m >> 6 & 63 | 128)
                e.append(m & 63 | 128)
    a = b
    for f in range(len(e)):
        a += int(e[f])
        a = google_RL(a, 美元b)
    a = google_RL(a, Zb)
    if b1:
        a ^= b1
    else:
        a ^= 0
    if 0 > a:
        a = (a & 2147483647) + 2147483647
    a %= 1E6
    return str(int(a)) + jd + str(int(a) ^ b)


def google_RL(a, b):
    t = 'a'
    Yb = '+'
    for c in range(0, len(b)-2, 3):
        d = b[c+2]
        if d >= t:
            d = ord(d[0]) - 87
        else:
            d = int(d)
        if b[c+1] == Yb:
            d = unsigned_right_shitf(a, d)
        else:
            d = int(a) << d
        if b[c] == Yb:
            a = int(a) + d & 4294967295
        else:
            a = int(a) ^ d
    return a


def googleTrans(req):
    trans = None
    fromLang = req[0]
    toLang = req[1]
    q = req[2]
    tk = google_TL(q)
    url = '/translate_a/single?client=t&sl='+fromLang+'&tl='+toLang+'&hl='+toLang+'&dt=bd&dt=ex&dt=ld&dt=md&dt=qc&dt=rw&dt=rm&dt=ss&dt=t&dt=at&ie=UTF-8&oe=UTF-8&source=sel&tk='\
        + tk+'&q='+urllib.parse.quote(q)
    try:
        trans = http.client.HTTPConnection('translate.google.cn')
        trans.request('GET', url, headers={
                      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'})
        response = trans.getresponse()
        result_all = response.read().decode("utf-8")
        print(result_all)
        print('translate.google.cn'+url)
        result = json.loads(result_all)
        # print(result[0][-1][-1]) #原文读音
        # print(result[0][0][1]) #原文
        # print()
        # print(result[0][-1][-2]) #结果读音
        # print(result[0][0][0]) #结果
        # if result[7]:
        #    print(result[7][1]) #罗马音转平假
    except Exception as e:
        print(e)
    finally:
        if trans:
            trans.close()

    if req[0] == 'ja-Latn':
        if req[1] == 'ja-Hrgn':
            return result[7][1]
        else:
            tk = google_TL(result[7][1])
            url = '/translate_a/single?client=t&sl=ja&tl='+toLang+'&hl='+toLang+'&dt=bd&dt=ex&dt=ld&dt=md&dt=qc&dt=rw&dt=rm&dt=ss&dt=t&dt=at&ie=UTF-8&oe=UTF-8&source=sel&tk='\
                + tk+'&q='+urllib.parse.quote(result[7][1])
            try:
                trans = http.client.HTTPConnection('translate.google.com')
                trans.request('GET', url)
                response = trans.getresponse()
                result_all = response.read().decode("utf-8")
                result = json.loads(result_all)
            except Exception as e:
                print(e)
            finally:
                if trans:
                    trans.close()
            if req[1] == 'ja':
                return result[7][1]
    return result[0][0][0]


def 能不能好好说话(*attrs, **kwargs):
    if attrs:
        return [Plain(hhsh(' '.join(attrs)))]
    else:
        return [Plain('宁想说什么？')]


def 咕狗翻译(*attrs, **kwargs):
    if ' '.join(attrs) in ('黙れ', '闭嘴', 'damare', 'E') or ' '.join(attrs[2:]) in ('黙れ', '闭嘴', 'damare', 'E'):
        del GLOBAL.QuickCalls[getPlayer(**kwargs)]
        return [Plain('我住嘴了')]
    if len(attrs) > 2:
        if attrs[2] == '=':
            GLOBAL.QuickCalls[getPlayer(
                **kwargs)] = (咕狗翻译, attrs[0], attrs[1])
            return [Plain(f'快速翻译打开（{attrs[0]}=>{attrs[1]},结束打E）')]
        return [Plain(text=googleTrans([attrs[0], attrs[1], ' '.join(attrs[2:])]))]
    else:
        return [Plain(text='原谅我不知道你在说什么（')]


def 百度翻译(*attrs, **kwargs):
    if ' '.join(attrs) in ('黙れ', '闭嘴', 'damare', 'E') or ' '.join(attrs[2:]) in ('黙れ', '闭嘴', 'damare', 'E'):
        del GLOBAL.QuickCalls[getPlayer(**kwargs)]
        return [Plain('我住嘴了')]
    if len(attrs) > 2:
        if attrs[2] == '=':
            GLOBAL.QuickCalls[getPlayer(
                **kwargs)] = (百度翻译, attrs[0], attrs[1])
            return [Plain(f'快速翻译打开（{attrs[0]}=>{attrs[1]},结束打E）')]
        return [Plain(text=BDtranslate([attrs[0], attrs[1], ' '.join(attrs[2:])]))]
    else:
        return [Plain(text='原谅我不知道你在说什么（\n')]


TranslateMap = {
    '#gkr':咕狗翻译,
    '#bkr':百度翻译,
    '#好好说话':能不能好好说话,
}

TranslateShort = {
    '#hhsh':'#好好说话','#kr':'#bkr',
}

TranslateDescript = {
    '#好好说话':'来自fufu的功能，如果有不懂的缩写可以用它查询，例:#好好说话 bksn',
    '#gkr':
"""
从fufu那里焊接来的咕狗翻译功能
格式：
    #gkr <源语言> <目标语言> <待翻译部分>
进入快速翻译模式（每句都处理）:
    #gkr <源语言> <目标语言> =
例：
    #gkr ja zh-CN やりますね

""",
    '#bkr':
"""
从fufu那里焊接来的度娘翻译功能
格式：
    #bkr <源语言> <目标语言> <待翻译部分>
进入快速翻译模式（每句都处理）:
    #bkr <源语言> <目标语言> =
例：
    #bkr jp zh 自分で百度しろ
""",
}


if __name__ == '__main__':
    req = []
    req.append('en')
    req.append('zh-CN')
    #req.append('わたしは だれですか？')
    req.append('Who I am?')
    print(googleTrans(req))
