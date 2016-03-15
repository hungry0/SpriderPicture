# -*- coding: utf-8 -*-

import urllib
import urllib2
import os
import re
import requests

class getPicAndDiviedDir(object):
    def getHtml(self,page):                 #获取网页内容
        header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36'}
        requeset = urllib2.Request(page, headers = header)
        response = urllib2.urlopen(requeset)
        return response.read()

    def getPicHtml(self,html):              #获取图片的路径list
        patternImg = re.compile('<img.*?src="(.*?)"',re.S)
        list = re.findall(patternImg,html)
        return list

    def getTitleHtml(self,html):            #获取标题，用于文件夹的名称
        patternTitle = re.compile('<title>(.*?)</title>',re.S)
        listTitle = re.findall(patternTitle,html)
        return listTitle

    def getPicAndDiv(self,listPic,title):   #输出图片，放置到规定文件夹下
        if len(title) > 0:
            path = title[0].decode('utf-8')
            if not os.path.exists(path):    #如果有当前目录，就会报错，以此判断
                os.mkdir(path)
        else:
            path = os.path.abspath('.')     #如果没有标题，则放置在当前目录下

        x = 0
        for each in listPic:
            print 'now downloading:',each
            pic = requests.get(each)
            fp = open(path + '/' + str(x) + '.jpg','wb')
            fp.write(pic.content)
            fp.close()
            x+=1

page = raw_input('Please input the website where you want to get pic: ')
assert page[0] != 'w','Please add http:// or https://'
obj = getPicAndDiviedDir()

html = obj.getHtml(page)
listPic = obj.getPicHtml(html)
print listPic
listTitle = obj.getTitleHtml(html)
obj.getPicAndDiv(listPic,listTitle)
