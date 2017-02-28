# -*- coding: utf-8 -*-
# !/bin/env python

'''
1、读取指定目录下的所有文件
2、读取指定文件，输出文件内容
3、创建一个文件并保存到指定目录
'''
import os,re


# 遍历指定目录，显示目录下的所有文件名
def eachFile(filepath):
    pathDir = os.listdir(filepath)
    for allDir in pathDir:
        child = os.path.join('%s%s' % (filepath, allDir))
        print child.decode('gbk')  # .decode('gbk')是解决中文显示乱码问题
        filename = child.decode('gbk')
        readFile(filename)
        #exit()


# 读取文件内容并打印
def readFile(filename):
    fopen = open(filename, 'r')  # r 代表read
    content = fopen.read()
    content = content.decode('gbk')
    #print "读取到得内容如下：", content
    findFile(content)
    '''for eachLine in fopen:
        print "读取到得内容如下：", eachLine'''
    fopen.close()

# 查找文件内容
def findFile(content):
    #查找标题
    p = '<title>.*</title>'
    match = re.search(p,content)
    title = match.group()
    title = title.replace(' ','')
    strinfo = re.compile('<title>|<.title>|-davidjory.*')
    title = strinfo.sub('', title)
    print title

# 输入多行文字，写入指定文件并保存到指定文件夹
def writeFile(filename):
    fopen = open(filename, 'w')
    print "\r请任意输入多行文字", " ( 输入 .号回车保存)"
    while True:
        aLine = raw_input()
        if aLine != ".":
            fopen.write('%s%s' % (aLine, os.linesep))
        else:
            print "文件已保存!"
            break
    fopen.close()


if __name__ == '__main__':
    filePath = "D:\\FileDemo\\Java\\myJava.txt"
    filePathI = "D:\\FileDemo\\Python\\pt.py"
    filePathC = "C:\\Users\\Administrator\\Downloads\\blog_articles\\"
    eachFile(filePathC)
    #readFile(filePath)
    #writeFile(filePathI)