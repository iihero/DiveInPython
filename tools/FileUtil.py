#-*- coding:utf-8 –*-

""" 用Python处理文档，总是碰到WindowsError这个提示，几经折腾，找到的原因如下：

WindowsError：[Error 2] 不存在这个文件

WindowsError：[Error 3] 没有这个路径

WindowsError：[Error 5] 权限问题

WindowsError：[Error 13] 该文档被其它程序占用，处理不了

WindowsError：[Error 123] 路径语法有误

WindowsError：[Error 145] 目录非空，多在删除非空目录时出现
--------------------- 
作者：Cacra 
来源：CSDN 
原文：https://blog.csdn.net/u014465934/article/details/73065723 
版权声明：本文为博主原创文章，转载请附上博文链接！ """

import os
from nt import chdir
import argparse
import sys
import math
import string
import re

# 以下import 用于中文排序
from ctypes import c_int, WINFUNCTYPE, windll
from ctypes.wintypes import LPCWSTR 

Shlwapi = windll.LoadLibrary("Shlwapi")
@WINFUNCTYPE(c_int, LPCWSTR, LPCWSTR)
def compare_string(first_str, second_str):
    return Shlwapi.StrCmpLogicalW(first_str, second_str)

def processParser():
    parser = argparse.ArgumentParser(description='Process some files')
    parser.add_argument('dir', help='target directory to process', default='.')
    parser.add_argument('-add', "--add", help='add number or not', choices=['true', 'false'], default='true')
    parser.add_argument('-start', '--start', help='First number', type=int, default=1)
    return parser

def tekan():
    i=1 #为序号赋初值
    for old_file in os.listdir('.'): #os.listfir('.')用于获取当前文件夹所有文件名，'.'表示当前文件夹，也可改为目标文件路径
        if 'py' not in old_file: #由于脚本文件不需要修改文件名，所以这里做个判断
            #new_name=old_file.split(' ')[1] #这行用来将文件名回到原来状态
            new_name=str(i)+'.'+str(old_file) #在文件名前加上序号与空格
            os.rename(old_file,new_name) #os.rename()用来修改名称
            i+=1 #序号加1
            
def tekan2(): # 将序号 减去一个值
    i=77 #为序号赋初值
    for old_file in os.listdir('.'): #os.listfir('.')用于获取当前文件夹所有文件名，'.'表示当前文件夹，也可改为目标文件路径
        if 'py' not in old_file: #由于脚本文件不需要修改文件名，所以这里做个判断
            #new_name=old_file.split(' ')[1] #这行用来将文件名回到原来状态
            fileName = str(old_file)
            fileName = fileName[fileName.find('.') : ]
            new_name=str(i-76)+fileName #在文件名前加上序号与空格
            os.rename(old_file,new_name) #os.rename()用来修改名称
            i+=1 #序号加1            

def isNumber(value): # something wrong
    try:
        value + 1
    except TypeError:
        return False
    else:
        return True

def removeDigitPrefixViaRe(str):
    return re.sub("\d", "", str, 4)

def removeDigitPrefix(str):
    return str.translate(None, string.digits)

def removeDotPrefix(str):
    # find the last '.', keep it
    rpos = str.rfind('.')
    if (rpos == -1):
        return str
    leftpart = str[0 : rpos]
    rightpart = str[rpos:]
    result =  re.sub("\.+", "", leftpart) + rightpart
    return result    
    

def isNumber2(value):
    try:
        x = int(value)
    except TypeError:
        return False
    except ValueError:
        return False
    except Exception, e:
        return False
    else:
        return True        


def removeNumbers(dir):
    chdir(dir)
    files = os.listdir(dir)
    # files.sort()
    files.sort(lambda x, y: compare_string(x, y))
    for old_file in files: 
        if 'py' not in old_file: 
            fileName = str(old_file)
            new_name = removeDigitPrefix(fileName)
            new_name = removeDotPrefix(new_name)
            print "old file: ", old_file, "=> new file: ", new_name
            os.rename(old_file, new_name)

def addNumbers(dir, start):
    i=start
    chdir(dir)
    files = os.listdir(dir)
    # files.sort()
    files.sort(lambda x, y: compare_string(x, y))
    for old_file in files: 
        fileName = str(old_file)
        new_name=str(i)+ '.' + fileName
        os.rename(old_file,new_name)
        print "remamed: ", old_file, " ==> ", new_name
        i+=1

def removeNumbers0(dir):
    chdir(dir)
    for old_file in os.listdir(dir): 
        if 'py' not in old_file: 
            fileName = str(old_file)
            number = fileName[0 : fileName.find('.')]
            print "number: ", number
            if (isNumber2(number)):
                subfilename = fileName[fileName.find('.') + 1 : ]
                fileName = subfilename[subfilename.find('.') : ]
                new_name=subfilename
                print "old file: ", old_file
                print "subfilename: ", subfilename
                print "new_name: ", new_name
                os.rename(old_file, new_name)
            else:
                print "number: ", number, "is not number"

if __name__ == '__main__':
    parser  = processParser()
    args = parser.parse_args()
    print "targit dir: ", args.dir
    print "start no: ", args.start
    print "add ?  ", args.add
    if (args.add == 'false'):
        removeNumbers(args.dir)
    else:
        addNumbers(args.dir, args.start)

