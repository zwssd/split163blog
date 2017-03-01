# -*- coding: utf-8 -*-
# !/bin/env python

'''
1、读取指定目录下的所有文件
2、读取指定文件，输出文件内容
3、创建一个文件并保存到指定目录
'''
import os,re

writeFilePath = "/Users/david/mypython/split163blog-git/git_articles/"

# 遍历指定目录，显示目录下的所有文件名
def eachFile(filepath):
    pathDir = os.listdir(filepath)
    for allDir in pathDir:
        child = os.path.join('%s%s' % (filepath, allDir))
        print child
        #print child.decode('gbk')  # .decode('gbk')是解决中文显示乱码问题
        #win下需要下面的转码
        #filename = child.decode('gbk')
        ext = os.path.splitext(child)[1]
        print ext
        if ext!='.htm':
            continue
        readFile(child)
        #exit()


# 读取文件内容并打印
def readFile(filename):
    fopen = open(filename, 'r')  # r 代表read
    fcontent = fopen.read()
    fcontent = fcontent.decode('gbk')
    #print "读取到得内容如下：", content
    findFile(fcontent)
    '''for eachLine in fopen:
        print "读取到得内容如下：", eachLine'''
    fopen.close()

# 查找文件内容
def findFile(fcontent):
    #查找标题
    p = '<title>(.*)</title>'
    match = re.search(p,fcontent)
    title = match.group()
    title = title.replace(' ','')
    strinfo = re.compile('<title>|<.title>|-davidjory.*')
    title = strinfo.sub('', title)
    print title
    #查找日期,分类
    res = 'class="blogsep">(.*?)</a>'
    date_category = re.findall(res,fcontent,re.S)[0]
    res = '(.*?)</span>'
    date = re.findall(res,date_category)[0]
    res = u'&nbsp;&nbsp;分类：</span>(.*)'
    category = re.findall(res,date_category,re.S)[0]
    category = filter_tags(category)
    category = category.replace('\n','')
    category = category.replace(' ','')
    category = category.replace('	','')
    print u'分类=======>>>>>>>>>>>>>'+category
    #查找标签
    #res = u'$_blogTagTitle">|&nbsp;&nbsp;标签：</span>(.*?)</span>'
    #tag = re.findall(res,fcontent)
    #print tag
    #print u'标签=======>>>>>>>>>>>>>'+tag
    #查找内容
    res = 'nbw-blog ztag">(.*)<div class="nbw-blog-end'
    content = re.findall(res,fcontent,re.S)[0]
    content = filter_tags(content)
    #print content
    writeFile(writeFilePath,title,date,category,content)

# 输入多行文字，写入指定文件并保存到指定文件夹
def writeFile(writeFilePath,title,date,category,content):
    ftitle = title.replace('.','')
    ftitle = ftitle.replace('/','')
    ftitle = ftitle.replace(' ','')
    fopen = open(writeFilePath+date[0:10]+'-'+ftitle+'.md', 'w')
    ftext = '''---
layout: post
title:  "'''+title+'''"
date:   '''+date+'''
categories: '''+category+'''
tags:
---

* content
{:toc}

'''+content+'''
'''
    #content.encode("utf8")
    fopen.write(ftext.encode("utf8"))
    fopen.close()

#将HTML中标签等信息去掉
#@param htmlstr HTML字符串.
def filter_tags(htmlstr):
    #先过滤CDATA
    re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #匹配CDATA
    re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
    re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style
    re_br=re.compile('<br\s*?/?>')#处理换行
    re_h=re.compile('</?\w+[^>]*>')#HTML标签
    re_comment=re.compile('<!--[^>]*-->')#HTML注释
    s=re_cdata.sub('',htmlstr)#去掉CDATA
    s=re_script.sub('',s) #去掉SCRIPT
    s=re_style.sub('',s)#去掉style
    s=re_br.sub('\n',s)#将br转换为换行
    s=re_h.sub('',s) #去掉HTML 标签
    s=re_comment.sub('',s)#去掉HTML注释
    #去掉多余的空行
    blank_line=re.compile('\n+')
    s=blank_line.sub('\n',s)
    s=replaceCharEntity(s)#替换实体
    return s


##替换常用HTML字符实体.
# 使用正常的字符替换HTML中特殊的字符实体.
# 你可以添加新的实体字符到CHAR_ENTITIES中,处理更多HTML字符实体.
# @param htmlstr HTML字符串.
def replaceCharEntity(htmlstr):
    CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
                     'lt': '<', '60': '<',
                     'gt': '>', '62': '>',
                     'amp': '&', '38': '&',
                     'quot': '"', '34': '"', }

    re_charEntity = re.compile(r'&#?(?P<name>\w+);')
    sz = re_charEntity.search(htmlstr)
    while sz:
        entity = sz.group()  # entity全称，如&gt;
        key = sz.group('name')  # 去除&;后entity,如&gt;为gt
        try:
            htmlstr = re_charEntity.sub(CHAR_ENTITIES[key], htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
        except KeyError:
            # 以空串代替
            htmlstr = re_charEntity.sub('', htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
    return htmlstr


if __name__ == '__main__':
    filePath = "D:\\FileDemo\\Java\\myJava.txt"
    filePathI = "D:\\FileDemo\\Python\\pt.py"
    #filePathC = "C:\\Users\\Administrator\\Downloads\\blog_articles\\"
    filePathC = "/Users/david/mypython/split163blog-git/blog_articles/"
    eachFile(filePathC)
    #readFile(filePath)
    #writeFile(filePathI)