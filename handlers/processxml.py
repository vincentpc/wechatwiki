# -*- coding:utf-8 -*-

import logging

from search.gsearch import GoogleAPI
from search.bsearch import BaiduAPI
from music.xmmusic import music_api
from finance.jsquery import query_fund, query_stock
from handlers.wechat import WeChat
import setting.settings as settings


def processXml(xml):
    wechat = WeChat(xml)
    help = settings.HELP
    about = settings.ABOUT
    if wechat.MsgType == 'event':
        if wechat.Event == 'CLICK':
            if wechat.EventKey == 'help':
                text = help
                response = wechat.textResp(content=text, funcflag=0)
            elif wechat.EventKey == 'about':
                text = about
                response = wechat.textResp(content=text, funcflag=0)
            else:
                text = help
                response = wechat.textResp(content=text, funcflag=0)

    elif wechat.MsgType == 'text':
        t = wechat.Content
        if t.startswith("fund"):
            data = query_fund(t[5:])
            if data:
                text = u"%s\nnet value: %s\ngrowth: %s" %\
                    (data['name'], data['newnet'], data['daygrowrate'])
            else:
                text = u"fund not exist"
            response = wechat.textResp(content=text, funcflag=0)
        elif t.startswith("stocksh"):
            data = query_stock(t[8:], 1)
            if data:
                text = u"%s\nreal price: %s\ngrowth: %s" %\
                    (data['name'], data['nowprice'], data['daygrowrate'])
            else:
                text = u"stock not exist"
            response = wechat.textResp(content=text, funcflag=0)
        elif t.startswith("stocksz"):
            data = query_stock(t[8:], 0)
            if data:
                text = u"%s\nreal price: %s\ngrowth: %s" %\
                    (data['name'], data['nowprice'], data['daygrowrate'])
            else:
                text = u"stock not exist"
            response = wechat.textResp(content=text, funcflag=0)
        elif t.startswith('g '):
            query = t[2:]
            api = GoogleAPI()
            result = api.search(query)
            itemlist = []
            for r in result:
                pic_item = wechat.make_pic(r.getTitle(),
                                           r.getContent(), "", r.getURL())
                itemlist.append(pic_item)
            response = wechat.picResp(itemlist, funcflag=0)
        elif t.startswith('b '):
            query = t[2:]
            api = BaiduAPI()
            result = api.search(query)
            itemlist = []
            for r in result:
                pic_item = wechat.make_pic(r.getTitle(),
                                           r.getContent(), "", r.getURL())
                itemlist.append(pic_item)
            response = wechat.picResp(itemlist, funcflag=0)
        elif t.startswith('m '):
            query = t[2:]
            api = music_api()
            result = api.getsong(query)
            if result:
                response = wechat.musicResp(
                    title=result.title, description=result.description,
                    url=result.url, hqurl=result.url, funcflag=0)
            else:
                response = None
        elif t.startswith('test'):
            data = t[5:]
            text = u"echo back: %s\n" % (data)  # echo back
            response = wechat.textResp(content=text, funcflag=0)
        else:
            text = help
            response = wechat.textResp(content=text, funcflag=0)
    else:
        text = help
        response = wechat.textResp(content=text, funcflag=0)

    return response
