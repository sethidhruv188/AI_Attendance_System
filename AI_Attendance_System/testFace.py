import pymysql
import face_recognition
import pickle

connection = pymysql.connect(host='127.0.0.1',user='root',passwd='sethidhruv188',database='faces',charset='utf8'
                             ,use_unicode=True)
cursor = connection.cursor()
