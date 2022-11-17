import json
import mysql.connector
from mysql.connector.pooling import MySQLConnectionPool
connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    user='root',
    password='',
    host='127.0.0.1',
    database='taipei_trip',
    pool_name = "taipei_pool",
    pool_size = 32,
    pool_reset_session = True,
)
from flask import *
with open("taipei-attractions.json",encoding="utf-8") as file:
    data=json.load(file)
    data_All=data["result"]["results"]
    for spot in data_All:
        id = spot["_id"]
        name = spot["name"]
        category = spot["CAT"]
        description = spot["description"]
        address = spot["address"]
        transport = spot["direction"]
        mrt = spot["MRT"]
        lat = spot["latitude"]
        lng = spot["longitude"]
        # print(lat)
        photo=spot["file"]
        photo_split=photo.split("https")
        photo_filter =list(filter(None, photo_split))
    
        # 和資料庫做互動
        connection_object = connection_pool.get_connection()
        mycursor = connection_object.cursor()
        # 檢查景點資訊是否存在 
        mycursor.execute('SELECT * FROM attraction WHERE id=%s or name =%s' ,(id, name))
        result = mycursor.fetchone()
        print(result)
        if result != None:
            print("資料已經傳入過")
        # 如果資料庫不存在則存入資料
        mycursor.execute("INSERT INTO attraction (id, name, category, description, address, transport, mrt, lat, lng) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)" ,(id, name, category, description, address, transport, mrt, lat, lng))
        connection_object.commit()
        print(mycursor.rowcount, "record inserted.")
        mycursor.close()
        connection_object.close()
    for photo_list in data_All:
        id = photo_list["_id"]
        photo=photo_list["file"]
        photo_split=photo.split("https")
        photo_filter =list(filter(None, photo_split))
        for i in range(0, len(photo_filter)):
            result="https"+photo_filter[i]
            if result.endswith('jpg') or result.endswith("JPG"):
                # 和資料庫做互動
                connection_object = connection_pool.get_connection()
                mycursor = connection_object.cursor()
                
                mycursor.execute("INSERT INTO photo (photo_id, photo) VALUES (%s, %s)" ,(id, result))
                connection_object.commit()
                print(mycursor.rowcount, "record inserted.")
                mycursor.close()
                connection_object.close()
               