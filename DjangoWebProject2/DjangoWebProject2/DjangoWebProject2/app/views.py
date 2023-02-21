"""
Definition of views.
"""

from telnetlib import IP
import pandas as pd
import mysql.connector
from mysql.connector import Error
import re
import pymysql
from datetime import datetime
from fileinput import filename
from http.client import HTTPResponse
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpRequest
from django.http import HttpResponse
import logging
import os
from django.conf import settings
from os import mkdir
from os.path import isdir, abspath, dirname, join

BASE_DIR = dirname(dirname(abspath(__file__)))

mydb = mysql.connector.connect(
    host='10.250.78.120',          # 主機名稱
    database='test', # 資料庫名稱
    user='carolwu',        # 帳號
    password='1qazXSW@')  # 密碼

cursor = mydb.cursor()
compile_ip=re.compile('^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$') #判斷是否為ip

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__) #<<<<<<<<<<<<<<<<<<<<

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def insert_and_delete(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/insert_and_delete.html',
        {
            'title':'update list',
            'message':'Insert to database and Delete from database',
            'year':datetime.now().year,
        }
    )

# 将excel数据写入mysql
#def get_con():
#    db = pymysql.connect(host='localhost',          
#    database='test', 
#    user='root',        
#    password='1qazXSW@')

#    return db

def wrdb(filename):
    # 打开上传 excel 表格
    ip_insert= 0
    ip_rept= 0 #ip數量計算
    domain_insert= 0
    domain_rept= 0 #domain數量計算
    ip_deleted = 0
    domain_deleted = 0 #刪除數量計算

    if filename=="附件八、N-ISAC 勒索軟體清單(2022-09-15).xlsx":
        df = pd.read_excel("/djg/Django/DjangoWebProject2/DjangoWebProject2/upload/"+filename, sheet_name="勒索軟體來源", usecols="B") 
        for index, row in df.iterrows():
            if row[0] != 'IP' and str(row[0]) !="nan":
                print(row[0])
        sure = input("確定要將以上清單新增置資料庫嗎?(Y/N) ")
        if sure == "Y":
            for index, row in df.iterrows():
                if row[0] != 'IP':
                    try:
                        if str(row[0]) !="nan":
                            cursor.execute("INSERT INTO `ip`(`IP`) VALUES ('"+str(row[0])+"');")
                            print(row[0],'此ip已新增')
                            mydb.commit()
                            ip_insert +=1 
                    except mysql.connector.errors.IntegrityError:
                            print(row[0],'此ip已重複')
                            ip_rept+=1
        else:
            print("已取消此動作")
        print("=====")
    elif filename=="附件三、中繼站IP與網域異動清單第37期(2022).xlsx":
        df = pd.read_excel("/djg/Django/DjangoWebProject2/DjangoWebProject2/upload/"+filename, sheet_name="IP異動", usecols="A") 
        for index, row in df.iterrows():
            if row[0] != '本週新增之惡意IP' and str(row[0]) !="nan":
                print(row[0])
        sure = input("確定要將以上清單新增置資料庫嗎?(Y/N) ")
        if sure == "Y":
                for index, row in df.iterrows():
                    if row[0] != '本週新增之惡意IP':        
                        try:
                            if str(row[0]) !="nan":
                                    cursor.execute("INSERT INTO `ip`(`IP`) VALUES ('"+str(row[0])+"');")
                                    print(row[0],'此ip已新增')
                                    mydb.commit()
                                    ip_insert +=1 
                        except mysql.connector.errors.IntegrityError:
                            print(row[0],'此ip已重複')
                            ip_rept+=1
        else:
            print("已取消此動作")
        print("=====")       
    elif filename=="附件九、N-ISAC中繼站列表(2022-09-15).xls":
        df = pd.read_excel("/djg/Django/DjangoWebProject2/DjangoWebProject2/upload/"+filename, sheet_name="IpList(order_by_Priority)", usecols="B") 
        for index, row in df.iterrows():
            if row[0] != 'IP-List' and str(row[0]) !="nan":
                print(row[0]) 
        sure = input("確定要將以上清單新增置資料庫嗎?(Y/N) ")
        if sure == "Y":
            for index, row in df.iterrows():
                if row[0] != 'IP-List':
                    try:
                        if str(row[0]) !="nan":
                            cursor.execute("INSERT INTO `ip`(`IP`) VALUES ('"+str(row[0])+"');")
                            print(row[0],'此ip已新增')
                            mydb.commit()
                            ip_insert +=1 
                    except mysql.connector.errors.IntegrityError:
                        print(row[0],'此ip已重複')
                        ip_rept+=1
        else:
            print("已取消此動作")
        print("=====")
    elif filename=="附件二、中繼站IP與網域清單第37期(2022).xlsx":
        df = pd.read_excel("/djg/Django/DjangoWebProject2/DjangoWebProject2/upload/"+filename, sheet_name="ip", usecols="B") 
        for index, row in df.iterrows():
            if row[0] != 'IP' and str(row[0]) !="nan":
                print(row[0])
        sure = input("確定要將以上清單新增置資料庫嗎?(Y/N) ")
        if sure == "Y":
            for index, row in df.iterrows():
                if row[0] != 'IP':
                    try:
                        if str(row[0]) !="nan":
                                    cursor.execute("INSERT INTO `ip`(`IP`) VALUES ('"+str(row[0])+"');")
                                    print(row[0],'此ip已新增')
                                    mydb.commit()
                                    ip_insert +=1 
                    except mysql.connector.errors.IntegrityError:
                        print(row[0],'此ip已重複')
                        ip_rept+=1
        else:
            print("已取消此動作")
        print("=====")

    ###Domain List
    if filename=="附件五、N-ISAC 釣魚網域清單(2022-09-15).xlsx":
        df = pd.read_excel("/djg/Django/DjangoWebProject2/DjangoWebProject2/upload/"+filename, sheet_name="釣魚網域", usecols="B") 
        for index, row in df.iterrows():
            if row[0] != 'fqdn' and str(row[0]) !="nan":
                print(row[0])
        sure = input("確定要將以上清單新增置資料庫嗎?(Y/N) ")
        if sure == "Y":
            for index, row in df.iterrows():
                if row[0] != 'fqdn':
                    try:
                        if str(row[0]) !="nan":
                                cursor.execute("INSERT INTO `domain`(`Domain`) VALUES ('"+str(row[0])+"');")
                                print(row[0],'此domain已新增')
                                mydb.commit()
                                domain_insert +=1 
                    except mysql.connector.errors.IntegrityError:
                        print(row[0],'此domain已重複')
                        domain_rept+=1
        else:
            print("已取消此動作")
        print("=====")
    elif filename=="附件六、N-ISAC 惡意網域清單(2022-09-15).xlsx":
        df = pd.read_excel("/djg/Django/DjangoWebProject2/DjangoWebProject2/upload/"+filename, sheet_name="惡意網域", usecols="B") 
        for index, row in df.iterrows():
            if row[0] != 'fqdn' and str(row[0]) !="nan":
                print(row[0])
        sure = input("確定要將以上清單新增置資料庫嗎?(Y/N) ")
        if sure == "Y":
            for index, row in df.iterrows():
                if row[0] != 'fqdn':
                    try:
                        if str(row[0]) !="nan":
                                cursor.execute("INSERT INTO `domain`(`Domain`) VALUES ('"+str(row[0])+"');")
                                print(row[0],'此domain已新增')
                                mydb.commit()
                                domain_insert +=1 
                    except mysql.connector.errors.IntegrityError:
                        print(row[0],'此domain已重複')
                        domain_rept+=1
        else:
            print("已取消此動作")
        print("=====")
    elif filename=="附件三、中繼站IP與網域異動清單第37期(2022).xlsx":
        df = pd.read_excel("/djg/Django/DjangoWebProject2/DjangoWebProject2/upload/"+filename, sheet_name="Domain異動", usecols="A") 
        for index, row in df.iterrows():
            if row[0] != '本週新增之惡意DN' and str(row[0]) !="nan":
                print(row[0])
        sure = input("確定要將以上清單新增置資料庫嗎?(Y/N) ")
        if sure == "Y":
            for index, row in df.iterrows():
                if row[0] != '本週新增之惡意DN':
                    try:
                        if str(row[0]) !="nan":
                                cursor.execute("INSERT INTO `domain`(`Domain`) VALUES ('"+str(row[0])+"');")
                                print(row[0],'此domain已新增')
                                mydb.commit()
                                domain_insert +=1 
                    except mysql.connector.errors.IntegrityError:
                        print(row[0],'此domain已重複')
                        domain_rept+=1
        else:
            print("已取消此動作")
        print("=====")
    elif filename=="附件九、N-ISAC中繼站列表(2022-09-15).xls":
        df = pd.read_excel("/djg/Django/DjangoWebProject2/DjangoWebProject2/upload/"+filename, sheet_name="DnList(order_by_Priority)", usecols="B") 
        for index, row in df.iterrows():
            if row[0] != 'Domain-List' and str(row[0]) !="nan":
                print(row[0])
        sure = input("確定要將以上清單新增置資料庫嗎?(Y/N) ")
        if sure == "Y":
            for index, row in df.iterrows():
                if row[0] != 'Domain-List':
                    try:
                        if str(row[0]) !="nan":
                                cursor.execute("INSERT INTO `domain`(`Domain`) VALUES ('"+str(row[0])+"');")
                                print(row[0],'此domain已新增')
                                mydb.commit()
                                domain_insert +=1 
                    except mysql.connector.errors.IntegrityError:
                        print(row[0],'此domain已重複')
                        domain_rept+=1
        else:
            print("已取消此動作")
        print("=====")
    elif filename=="附件二、中繼站IP與網域清單第37期(2022).xlsx":
        df = pd.read_excel("/djg/Django/DjangoWebProject2/DjangoWebProject2/upload/"+filename, sheet_name="domain", usecols="B") 
        for index, row in df.iterrows():
            if row[0] != "" and str(row[0]) !="nan":
                print(row[0])
        sure = input("確定要將以上清單新增置資料庫嗎?(Y/N) ")
        if sure == "Y":
            for index, row in df.iterrows():
                if row[0] != 'Domain':
                    try:
                        if str(row[0]) !="nan":
                                cursor.execute("INSERT INTO `domain`(`Domain`) VALUES ('"+str(row[0])+"');")
                                print(row[0],'此domain已新增')
                                mydb.commit()
                                domain_insert +=1 
                    except mysql.connector.errors.IntegrityError:
                        print(row[0],'此domain已重複')
                        domain_rept+=1
        else:
            print("已取消此動作")
        print("=====")

    ### IP and Domain List
    if filename=="附件七、N-ISAC APT 來源清單(2022-09-15).xlsx":
        df = pd.read_excel("/djg/Django/DjangoWebProject2/DjangoWebProject2/upload/"+filename, sheet_name="APT攻擊來源", usecols="B") 
        for index, row in df.iterrows():
            if row[0] != '來源' and str(row[0]) !="nan":
                print(row[0])
        sure = input("確定要將以上清單新增置資料庫嗎?(Y/N) ")
        if sure == "Y":
            for index, row in df.iterrows():
                if row[0] != '來源':
                    try:
                        if str(row[0]) !="nan":
                            if compile_ip.match(row[0]):
                                cursor.execute("INSERT INTO `ip`(`IP`) VALUES ('"+str(row[0])+"');")
                                print(row[0],'此ip已新增')
                                mydb.commit()
                                ip_insert +=1
                            else:
                                    try:
                                        cursor.execute("INSERT INTO `domain`(`Domain`) VALUES ('"+str(row[0])+"');")
                                        print(row[0],'此domain已新增')
                                        mydb.commit()
                                        domain_insert +=1
                                    except mysql.connector.errors.IntegrityError:
                                        print(row[0],'此domain已重複')
                                        domain_rept+=1
                    except mysql.connector.errors.IntegrityError:
                        print(row[0],'此ip已重複')
                        ip_rept+=1
        else:
            print("已取消此動作")
        print("=====")

    print("====================")
    print(ip_rept, "筆ip已重複")
    print(ip_insert, "筆ip已新增")
    print(ip_deleted, "筆ip已刪除")
    print("===")
    print(domain_rept, "筆domain已重複")
    print(domain_insert, "筆domain已新增")
    print(domain_deleted, "筆domain已刪除")
    print("===")


    print("====================")
    print(ip_rept, "筆ip已重複")
    print(ip_insert, "筆ip已新增")
    print(ip_deleted, "筆ip已刪除")
    print("===")
    print(domain_rept, "筆domain已重複")
    print(domain_insert, "筆domain已新增")
    print(domain_deleted, "筆domain已刪除")
    print("===")

def upload(request):
    # 根name取 file 的值
    file = request.FILES.get('file')
    print('uplaod:%s'% file)
    # 创建upload文件夹
    if not os.path.exists(settings.UPLOAD_ROOT):
        os.makedirs(settings.UPLOAD_ROOT)
    try:
        if file is None:
            return HttpResponse('請選擇要上傳的文件')
        # 循环二进制写入
        with open(settings.UPLOAD_ROOT + "/" + file.name, 'wb') as f:
            for i in file.readlines():
                f.write(i)
       
        # 写入 
        wrdb(file.name)
        return HttpResponse('已執行動作')

    except Exception as e:
        return HttpResponse(e)

def update_EDL(request):
    sure = input("確定將資料庫資料更新至EDL List中?(Y/N) ")
    if sure == "Y":
        try:
            # 連接 MySQL/MariaDB 資料庫
            mydb = mysql.connector.connect(
            host='10.250.78.120',          # 主機名稱
            database='test', # 資料庫名稱
            user='root',        # 帳號
            password='1qazXSW@')  # 密碼
            cursor = mydb.cursor()

            # 查詢資料庫
            cursor = mydb.cursor(buffered=True)
            cursor.execute("SELECT IP FROM ip;") 

            cursor2 =mydb.cursor(buffered=True)
            cursor2.execute("SELECT Domain FROM domain")

            # 取回全部的資料
            records = cursor.fetchall()
            records2 = cursor2.fetchall()
            print("資料庫IP 資料筆數：", cursor.rowcount)
            print("資料庫Domain 資料筆數：", cursor2.rowcount)

        except Error as e:
            print("資料庫連接失敗：", e)
    else:
        print("已取消動作")