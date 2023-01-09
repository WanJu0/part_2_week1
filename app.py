import json
import jwt
import requests
from flask import jsonify
import mysql.connector
from mysql.connector.pooling import MySQLConnectionPool
from mySQL import MySQLPassword
from datetime import datetime, timedelta
import datetime
import random
import base64
from dotenv import load_dotenv
load_dotenv()
import os
import boto3 

mysql_username = os.getenv("MYSQL_USERNAME")
mysql_password = os.getenv("MYSQL_PASSWORD")
mysql_host = os.getenv("MYSQL_HOST")
mysql_database = os.getenv("MYSQL_DATABASE")

connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    user=mysql_username,
    password=mysql_password,
    host=mysql_host,
    database=mysql_database ,
    pool_name = "taipei_pool",
    pool_size = 32,
    pool_reset_session = True,
)
from flask import *
app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
import json

# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")
@app.route("/member")
def member():
	return render_template("member.html")
@app.route("/api/attraction",methods=["GET"])
def api_attraction():
	
    connection_object = connection_pool.get_connection()
    mycursor=connection_object.cursor()
    page = int(request.args.get("page","0"))
    keyword = request.args.get("keyword","")
    try:
        if keyword == "":
            mycursor.execute("SELECT * FROM attraction LIMIT %s ,%s",(page*12,12))
            result = mycursor.fetchall()
           
        else:
            # 模糊比對景點名稱或分類完全比對
            mycursor.execute("SELECT * FROM attraction WHERE category=%s or name LIKE %s LIMIT %s ,%s",(keyword ,"%"+keyword+"%", page*12, 12))
            result = mycursor.fetchall()
            # print(result)
        if result != None:
            data_value=[]
            for i in range(0,len(result)):
                id= result[i][0]
                name = result[i][1]
                category = result[i][2]
                description = result[i][3]
                address = result[i][4]
                transport = result[i][5]
                mrt = result[i][6]
                lat = result[i][7]
                lng = result[i][8]
                
                # 圖片處理
                mycursor.execute("SELECT group_concat(photo) FROM attraction INNER JOIN photo ON attraction.id=photo.photo_id WHERE attraction.id=%s group by photo.photo_id" ,(id,))
                photo = mycursor.fetchone()
                
                photo_str = photo[0].split(',')
                attraction_list={
                    "id":id ,
                    "name":name,
                    "category":category,
                    "description":description,
                    "address":address,
                    "transport":transport,
                    "mrt":mrt,
                    "lat":lat,
                    "lng":lng,
                    "images":photo_str
                }
                data_value.append(attraction_list)	
                if len(result)<12:
                    next_Page=None
                else:
                    next_Page=page+1
            if data_value==[]:
                data={

                "nextPage":None ,
                "data":data_value
                }
                json_result=jsonify(data)
                mycursor.close()
                connection_object.close()
                return json_result,200
            data={

                "nextPage": next_Page,
                "data":data_value
            }
            json_result=jsonify(data)
            mycursor.close()
            connection_object.close()
            return json_result,200
    except:
        data={
            "error": True,
            "message":"伺服器內部錯誤"
        }
        json_result=jsonify(data)
        mycursor.close()
        connection_object.close()
        return json_result,500
    
@app.route("/api/attraction/<attractionID>",methods=["GET"])      
def attraction_ID(attractionID):
    connection_object = connection_pool.get_connection()
    mycursor=connection_object.cursor()
    try:
        mycursor.execute("SELECT * FROM attraction WHERE id=%s",(attractionID,))
        result = mycursor.fetchone()
        # print(type(result))
        if result != None:
            id= result[0]
            name = result[1]
            category = result[2]
            description = result[3]
            address = result[4]
            transport = result[5]
            mrt = result[6]
            lat = result[7]
            lng = result[8]
            
            # 圖片處理
            mycursor.execute("SELECT GROUP_CONCAT(CONCAT(photo)) FROM attraction INNER JOIN photo ON attraction.id=photo.photo_id WHERE attraction.id=%s GROUP BY photo.photo_id" ,(attractionID,))
            photo = mycursor.fetchone()
            # print(photo[0])
            photo_str = photo[0].split(',')
            # print(photo_str)
           
            attraction_list={
                "id":id ,
                "name":name,
                "category":category,
                "description":description,
                "address":address,
                "transport":transport,
                "mrt":mrt,
                "lat":lat,
                "lng":lng,
                "images":photo_str
            }
            
            data={
                "data":attraction_list
            }
			
            json_result=jsonify(data)
            # print(json_result)
            mycursor.close()
            connection_object.close()
            return json_result
        else:
            data={
            "error": True,
            "message":"編號不存在"
            }
            json_result=jsonify(data)
            mycursor.close()
            connection_object.close()
            return json_result,400
            
    except:
        data={
            "error": True,
            "message":"伺服器錯誤"
        }
        json_result=jsonify(data)
        mycursor.close()
        connection_object.close()
        return json_result,500
@app.route("/api/categories",methods=["GET"])
def categories():
    connection_object = connection_pool.get_connection()
    mycursor=connection_object.cursor()
    try:
        
        mycursor.execute("SELECT DISTINCT category FROM attraction")
        result = mycursor.fetchall()
       
        category_result=[]
        for x in range(0,len(result)):
            category=list(result[x])
            categories_list=category[0]
            category_result.append(categories_list)
        
        data={
            "data":category_result
        }
        json_result=jsonify(data)
        # print(json_result)
        mycursor.close()
        connection_object.close()
        return json_result
            
    except:
        data={
            "error": True,
            "message":"伺服器錯誤"
        }
        json_result=jsonify(data)
        mycursor.close()
        connection_object.close()
        return json_result,500

@app.route("/api/user",methods=["POST"])
def signup():
    # 從前端接收資料
    name=request.json["name"]
    email=request.json["email"]
    password=request.json["password"]
    #註冊帳號密碼不能為空
    if name=="" or email=="" or password=="":
        data={
            "error":True,
            "message":"請輸入帳號密碼"
        }
        json_result=jsonify(data)
        return json_result,400
    
    # 和資料庫做互動
    connection_object = connection_pool.get_connection()
    mycursor = connection_object.cursor()
    try:
        # 檢查姓名 帳號是否存在
        mycursor.execute('SELECT * FROM member WHERE name=%s or email =%s ' ,(name, email))
        result = mycursor.fetchone()
        # print(result)
        if result != None:
            data={
                "error":True,
                "message":"帳號已經存在"
            }
            json_result=jsonify(data)
            mycursor.close()
            connection_object.close()
            return json_result,400
        # 把資料放進資料庫 完成註冊
        mycursor.execute("INSERT INTO member (name, email, password ) VALUES (%s, %s, %s)" ,(name,email,password))
        connection_object.commit()
        print(mycursor.rowcount, "record inserted.")
        data={
            "ok":True,
        }
        # print(data)
        json_result=jsonify(data)
        mycursor.close()
        connection_object.close()
        return json_result, 200
    except:
        data={
            "error": True,
            "message":"伺服器錯誤"
        }
        json_result=jsonify(data)
        mycursor.close()
        connection_object.close()
        return json_result,500
# 登入系統！
@app.route("/api/user/auth",methods=["PUT"])
def signin():   
    email=request.json["email"]
    password=request.json["password"]
    #登入帳號密碼不能為空
    if email=="" or password=="":
        data={
            "error":True,
            "message":"請輸入帳號密碼"
        }
        # print(data)
        json_result=jsonify(data)
        return json_result,400
    # 和資料庫做互動
    connection_object = connection_pool.get_connection()
    mycursor = connection_object.cursor()
    try:
        # 檢查帳號密碼是否正確
        mycursor.execute('SELECT * FROM member WHERE email=%s AND password =%s' ,(email, password))
        result = mycursor.fetchone()
        # print(result)
        if result==None:
            mycursor.close()
            connection_object.close()
            data={
                "error":True,
                "message":"帳號密碼有誤"
            }
            # print(data)
            json_result=jsonify(data)
            return json_result,400
        # 用jwt產生token
        
        encoded_jwt = jwt.encode({
            "id":result[0],
            "name":result[1],
            "email":result[2],
            # "exp": datetime.utcnow() + timedelta(minutes=1)
            },"secretJWT", algorithm='HS256')
        # print(encoded_jwt)
        data={
            "ok":True,
        }
        
        response = make_response(jsonify(data))
        response.set_cookie(key="Set-Cookie", value=encoded_jwt, max_age=604800)
        json_result=jsonify(data)
        mycursor.close()
        connection_object.close()
        return response,200
        
    except:
        data={
            "error": True,
            "message":"伺服器錯誤"
        }
        json_result=jsonify(data)
        mycursor.close()
        connection_object.close()
        return json_result,500

@app.route("/api/user/auth",methods=["GET"])
def signin_get():
    cookie=request.cookies.get("Set-Cookie")
    if cookie != None:
        decode= jwt.decode(cookie, "secretJWT", ['HS256'])
        # print(decode)
        data={
            "data":decode
        }
        json_result=jsonify(data)
        return json_result
    data={
            "data":False
    }
    json_result=jsonify(data)
    return json_result

@app.route("/api/user/auth",methods=["DELETE"])
def signout():  
    data={
        "ok":True
    }
    response = make_response(jsonify(data))
    response.set_cookie(key="Set-Cookie", value="", max_age=-1)

    return response,200

@app.route("/api/booking",methods=["POST"])
def apiBooking():
    # 從前端接收資料
   
    attraction=request.json["attraction"]
    date=request.json["date"]
    time=request.json["time"]
    price=request.json["price"]
    # 一定要先登入,先檢查是否有登入
    cookie=request.cookies.get("Set-Cookie")
    print(cookie)
    if cookie != None:
        decode= jwt.decode(cookie, "secretJWT", ['HS256'])
        member_id=decode["id"]
        member_name=decode["name"]
        # 每個資料都不能為空
        if time=="" or date=="":
            data={
                "error":True,
                "message":"請選擇日期和時間"
            }
            json_result=jsonify(data)
            return json_result,400
        # 和資料庫做互動
        connection_object = connection_pool.get_connection()
        mycursor = connection_object.cursor()
        # 這邊要把資料放進去資料庫,並回傳狀態
        try:
            mycursor.execute("INSERT INTO reservation (member_id, attraction_id, date, time, price) VALUES (%s, %s, %s, %s, %s)" ,(member_id,attraction, date, time, price))
            connection_object.commit()
            print(mycursor.rowcount, "record inserted.")
            data={
                "ok":True,
            }
           
            json_result=jsonify(data)
            mycursor.close()
            connection_object.close()
            return json_result, 200
        except:
            data={
                "error": True,
                "message":"伺服器錯誤"
            }
            json_result=jsonify(data)
            mycursor.close()
            connection_object.close()
            return json_result,500
    else:
        data={
                "error":True,
                "message":"請先登入會員"
            }
        
        json_result=jsonify(data)
        return json_result,403
@app.route("/api/booking",methods=["GET"])
def getBooking():
    # 一定要先登入,先檢查是否有登入
    cookie=request.cookies.get("Set-Cookie")
    # print(cookie)
    if cookie != None:
        decode= jwt.decode(cookie, "secretJWT", ['HS256'])
        member_id=decode["id"]
        member_name=decode["name"]
        # print(member_name)
        # 和資料庫做互動
        connection_object = connection_pool.get_connection()
        mycursor = connection_object.cursor()
        # 還需要利用attraction id 去抓出景點資訊
        mycursor.execute('SELECT attraction.id, attraction.name,attraction.address,reservation.reservation_id,reservation.member_id,reservation.date,reservation.time,reservation.price FROM attraction INNER JOIN reservation ON attraction.id=reservation.attraction_id WHERE member_id=%s' ,(member_id,))
        result = mycursor.fetchall()
        if result != None:
            data_value=[]
            for i in range(0,len(result)):
                attraction_id=result[i][0]
                attraction_name=result[i][1]
                attraction_address=result[i][2]
                reservation_id=result[i][3]
                date=result[i][5]
                time=result[i][6]
                price=result[i][7]
                # 圖片處理
                mycursor.execute("SELECT group_concat(photo) FROM attraction INNER JOIN photo ON attraction.id=photo.photo_id WHERE attraction.id=%s group by photo.photo_id" ,(attraction_id,))
                photo = mycursor.fetchone()
                # print(photo)
                photo_str = photo[0].split(',')
                # print(photo_str[0])
                data={
                    
                    "attraction":{
                        "id":attraction_id,
                        "name":attraction_name,
                        "address":attraction_address,
                        "image":photo_str[0]
                    },
                    "date":str(date),
                    "time":time,
                    "price":price,
                    "reservationID":reservation_id
                    
                }
                data_value.append(data)	

            data={

                "data":data_value
            }
            
            json_result=jsonify(data)
            # print(json_result)
            mycursor.close()
            connection_object.close()
            return make_response(json_result,200)  
            # return data, 200
        else:
            data={

                "data":None
            }
            json_result=jsonify(data)
            # print(json_result)
            mycursor.close()
            connection_object.close()
            return make_response(json_result,200)  
    else:
        data={
                "error":True,
                "message":"請先登入會員"
            }
        # print(data)
        json_result=jsonify(data) 
        return make_response(json_result,403)  
@app.route("/api/booking",methods=["DELETE"])
def deleteBooking():
    reservation_id=request.json["reservationID"]
    print(reservation_id,"llll")
    # 一定要先登入,先檢查是否有登入
    cookie=request.cookies.get("Set-Cookie")
    # print(cookie)
    if cookie != None:
        decode= jwt.decode(cookie, "secretJWT", ['HS256'])
        member_id=decode["id"]
        member_name=decode["name"]
        # print(member_name)
        # 和資料庫做互動
        connection_object = connection_pool.get_connection()
        mycursor = connection_object.cursor()
        mycursor.execute("DELETE FROM reservation WHERE reservation_id=%s " ,(reservation_id,))
        connection_object.commit()
        print(mycursor.rowcount, "record inserted.")
        if mycursor.rowcount !=0:
            data={
                "ok":True,
            }
            json_result=jsonify(data) 
            mycursor.close()
            connection_object.close()
            return make_response(json_result,200)  
        else:
            data={
                "error":True,
                "message":"請在刪除一次"
            }
            # print(data)
            json_result=jsonify(data) 
            mycursor.close()
            connection_object.close()
            return make_response(json_result,403)  
       
       
    else:
        data={
                "error":True,
                "message":"請先登入會員"
            }
        # print(data)
        json_result=jsonify(data) 
        return make_response(json_result,403)  
@app.route("/api/orders",methods=["POST"])
def apiOrders():
    # 一定要先登入,先檢查是否有登入
    cookie=request.cookies.get("Set-Cookie")
    if cookie != None:
        decode= jwt.decode(cookie, "secretJWT", ['HS256'])
        member_id=decode["id"]
        member_name=decode["name"]
        # 從前端接收資料
    
        # 預定訂單編號的所有列表
        
        reservationNum=len(request.json["order"]["trip"])
        prime=request.json["prime"]
        total_price=request.json["order"]["price"]
        name=request.json["order"]["contact"]["name"]
        email=request.json["order"]["contact"]["email"]
        phone=request.json["order"]["contact"]["phone"]
        payment_status="未付款"
        # 產生當下日期時間
        now = datetime.datetime.now()
        # 產生六位隨機號碼
        rand = ''.join(str(random.randint(0, 9)) for _ in range(6))
        # 將日期時間和隨機號碼組合成訂單編號
        order_number = f"{now.strftime('%Y%m%d%H%M%S')}{rand}"
        print(order_number)
        
        # 每個資料都不能為空
        if name=="" or email=="" or phone=="":
            data={
                "error":True,
                "message":"請正確填寫姓名,信箱,電話"
            }
            # print(data)
            json_result=jsonify(data)
            return make_response(json_result,400)  
        for i in range(0,reservationNum):
            reservation_id=request.json["order"]["trip"][i]["reservationID"]
            attraction_id=request.json["order"]["trip"][i]["attraction"]["id"]
            date=request.json["order"]["trip"][i]["date"]
            time=request.json["order"]["trip"][i]["time"]
            price=request.json["order"]["trip"][i]["price"]
            connection_object = connection_pool.get_connection()
            mycursor = connection_object.cursor()
            try:
                mycursor.execute("INSERT INTO order_model(order_number, member_id, phone, attraction_id, date, time, price, payment_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)" ,(order_number, member_id, phone, attraction_id, date, time, price, payment_status))
                connection_object.commit()
                print(mycursor.rowcount, "record inserted.")

                # # 成立order訂單的同時刪除 booking裡的預定資訊(用reservationID刪除)
                mycursor.execute("DELETE FROM reservation WHERE reservation_id=%s " ,(reservation_id,))
                connection_object.commit()
                print(mycursor.rowcount, "record delete.")

                return "更新成功",200
            except:
                data={
                    "error": True,
                    "message":"伺服器錯誤"
                }
                json_result=jsonify(data)
                mycursor.close()
                connection_object.close()
                return json_result,500
        
        # 然後進入tappay api
        partner_key = os.getenv("TAPPAY_PARTNER_KEY")
        mydata={
            "prime":prime,
            "partner_key": partner_key,
            "merchant_id": "t2roioaui_CTBC",
            "details":"TapPay Test",
            "amount":int(total_price),
            "cardholder": {
                "phone_number": phone,
                "name": name,
                "email": email,
            },    
        }
        myheaders={
            "content-type":"application/json",
            "x-api-key": partner_key,
        }
        response=requests.post("https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime",headers=myheaders,json= mydata).json()
        print(response["status"])
        print(response)
        # 如果匯款成功,則傳訂單編號給前端並顯示訂單完成
        if response["status"] ==0:
            new_status="已付款"
            # 產生當下日期時間
            paymentTime = datetime.datetime.now()
            try:
                mycursor.execute("UPDATE order_model SET payment_status=%s, payment_time=%s WHERE order_number=%s" ,(new_status, paymentTime, order_number,))
                connection_object.commit()
                data={
                    "data": {
                        "number": order_number,
                        "payment": {
                        "status": 0,
                        "message": "付款成功"
                        }
                    }
                }
                json_result=jsonify(data) 
                mycursor.close()
                connection_object.close()
                return make_response(json_result,200)  
            except:
                data={
                    "error": True,
                    "message":"伺服器錯誤"
                }
                json_result=jsonify(data)
                mycursor.close()
                connection_object.close()
                return json_result,500
        else:
            data={
                "data": {
                    "number": order_number,
                    "payment": {
                    "status": response["status"],
                    "message": response["msg"]
                    }
                }
            }
            # print(data)
            json_result=jsonify(data) 
            mycursor.close()
            connection_object.close()
            return make_response(json_result,400)  
    else:
        data={
                "error":True,
                "message":"請先登入會員"
            }
        # print(data)
        json_result=jsonify(data)
        return json_result,403
@app.route("/api/orders/<orderNumber>",methods=["GET"])
def getOrders(orderNumber):
    # 一定要先登入,先檢查是否有登入
    cookie=request.cookies.get("Set-Cookie")
    # print(cookie)
    if cookie != None:
        decode= jwt.decode(cookie, "secretJWT", ['HS256'])
       
        member_id=decode["id"]
        member_name=decode["name"]
        member_email=decode["email"]
        connection_object = connection_pool.get_connection()
        mycursor=connection_object.cursor(dictionary=True)
        try:
            mycursor.execute("SELECT * FROM order_model JOIN attraction ON order_model.attraction_id=attraction.id WHERE order_number=%s",(orderNumber,))
            result = mycursor.fetchall()
            # 將訂購總金額計算出來
            mycursor.execute("SELECT SUM(price) FROM order_model JOIN attraction ON order_model.attraction_id=attraction.id WHERE order_number=%s",(orderNumber,))
            total= mycursor.fetchone()
           
            # 這邊先將
            if result != None:

                data_value=[]
                attraction_id=result[0]["attraction_id"]
                attraction_name=result[0]["name"]
                attraction_address=result[0]["address"]
                data_value=[]
                for i in range(0,len(result)):
                    attraction_id=result[i]["attraction_id"]
                    attraction_name=result[i]["name"]
                   
                    # 圖片處理
                    mycursor.execute("SELECT group_concat(photo) FROM attraction INNER JOIN photo ON attraction.id=photo.photo_id WHERE attraction.id=%s group by photo.photo_id" ,(attraction_id,))
                    photo = mycursor.fetchone()
                    photo_str = photo["group_concat(photo)"].split(',')
                    data={
                        "attraction":{
                            "id":result[i]["attraction_id"],
                            "name":result[i]["name"],
                            "address":result[i]["address"],
                            "image":photo_str[0],
                            "price":result[i]["price"]
                        },
                        "date":str(result[i]["date"]),
                        "time":result[i]["time"]
                    }
                    data_value.append(data)	
                data={
                    "data":{
                        "number":orderNumber,
                        "price":int(total["SUM(price)"]),
                        "trip":data_value
                    },
                    "contact":{
                        "name":member_name,
                        "email":member_email,
                        "phone":result[0]["phone"]
                    }
                }
                json_result=jsonify(data)
                # print(json_result)
                mycursor.close()
                connection_object.close()
                return make_response(json_result,200) 
                # return "111" 
            else:
                data={
                "error": True,
                "message":"編號不存在"
                }
                json_result=jsonify(data)
                mycursor.close()
                connection_object.close()
                return json_result,400
                
        except Exception as e:
            # print(e)
            data={
                "error": True,
                "message":"伺服器錯誤"
            }
            json_result=jsonify(data)
            mycursor.close()
            connection_object.close()
            return json_result,500
    else:
        data={
                "error":True,
                "message":"請先登入會員"
            }
        # print(data)
        json_result=jsonify(data) 
        return make_response(json_result,403)  
@app.route("/api/historyOrders/<memberID>",methods=["GET"])
def historyOrders(memberID):
    # 一定要先登入,先檢查是否有登入
    cookie=request.cookies.get("Set-Cookie")
    # print(cookie)
    if cookie != None:
        decode= jwt.decode(cookie, "secretJWT", ['HS256'])
        memberId=decode["id"]
        member_name=decode["name"]
        member_email=decode["email"]
        connection_object = connection_pool.get_connection()
        mycursor=connection_object.cursor(dictionary=True)
        try:
            mycursor.execute("SELECT member_id, GROUP_CONCAT(DISTINCT order_number) AS order_numbers FROM order_model WHERE member_id=%s GROUP BY member_id ; ",(memberID,))
            result = mycursor.fetchone()

            if result != None:
                history_list = result["order_numbers"].split(',')
                data={
                    "history_list":history_list
                }
                json_result=jsonify(data)
                mycursor.close()
                connection_object.close()
                return make_response(json_result,200) 
            else:
                data={
                "history_list":None
                }
                json_result=jsonify(data)
                mycursor.close()
                connection_object.close()
                return json_result,200
                
        except:
            data={
                "error": True,
                "message":"伺服器錯誤"
            }
            json_result=jsonify(data)
            mycursor.close()
            connection_object.close()
            return json_result,500
    else:
        data={
                "error":True,
                "message":"請先登入會員"
            }
        # print(data)
        json_result=jsonify(data) 
        return make_response(json_result,403)  
# 連接到aws s3
client = boto3.client('s3')
print(client,"123")
s3 = boto3.resource('s3',
    aws_access_key_id="AKIATJVY3KFA4E7LPCN2",
    aws_secret_access_key="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",
    region_name="ap-northeast-1")
for bucket in s3.buckets.all():
    print(bucket.name)
   
# Upload a new file
# s3.Bucket('taipeibucket').put_object(Key='test.jpg', Body=data)
@app.route("/api/images",methods=["POST"])
def updateImg():
# 一定要先登入,先檢查是否有登入
    cookie=request.cookies.get("Set-Cookie")
    # print(cookie)
    if cookie != None:
        decode= jwt.decode(cookie, "secretJWT", ['HS256'])
        memberId=decode["id"]
        member_name=decode["name"]
        member_email=decode["email"]
        img=request.files["img"]
        s3.Bucket('taipeibucket').put_object(Key=img.filename, Body=img)
        return "上傳成功"  
    else:
        data={
                "error":True,
                "message":"請先登入會員"
            }
        # print(data)
        json_result=jsonify(data) 
        return make_response(json_result,403)  
@app.route("/api/images",methods=["GET"])
def checkImg():
    # 一定要先登入,先檢查是否有登入
    cookie=request.cookies.get("Set-Cookie")
    # print(cookie)
    if cookie != None:
        decode= jwt.decode(cookie, "secretJWT", ['HS256'])
        memberId=decode["id"]
        member_name=decode["name"]
        member_email=decode["email"]
        key =str(memberId) + ".jpg"

        try:
            obj=s3.Object(bucket_name="taipeibucket", key=key)
            # print(obj)
            response = obj.get()
            # print(response,"obj")

            image_data = response['Body'].read()
            base64_data = base64.b64encode(image_data).decode()
            base64_data = "data:image/jpeg;base64," + base64_data
            # data={
            #     "image":base64_data,
            # }
            # json_result=jsonify(data) 
            
            return make_response(base64_data,200)  
            
        except Exception as e:
            # print(f'圖片 {key} 不存在')
            # print(e)
            # data={
            #     "image":None,
            # }
            # json_result=jsonify(data)
            return "False" 
    else:
        data={
                "error":True,
                "message":"請先登入會員"
            }
        # print(data)
        json_result=jsonify(data) 
        return make_response(json_result,403)  

# 會員頁面資料更新api
@app.route("/api/member",methods=["POST"])
def apiMembers():
     # 一定要先登入,先檢查是否有登入
    cookie=request.cookies.get("Set-Cookie")
    if cookie != None:
        decode= jwt.decode(cookie, "secretJWT", ['HS256'])
        member_id=decode["id"]
        member_name=decode["name"]
        # 從前端接收資料
        #前端接收資料
        data=request.json
        name=request.json["name"]
        email=request.json["email"]
        phone=request.json["phone"]
        birthday=request.json["birthday"]
        emergencyName=request.json["emergencyName"]
        emergencyPhone=request.json["emergencyPhone"]
        gender=request.json["gender"]
        # print(data)
        # print(name)
        # print(email)
        # print(phone)
        # print(birthday)
        # print(emergencyName)
        # print(emergencyPhone)
        # print(gender)
        connection_object = connection_pool.get_connection()
        mycursor = connection_object.cursor()
        try:
            mycursor.execute("UPDATE member SET name=%s, email=%s, member_phone=%s, birthday=%s, emergency_name=%s, emergency_phone=%s, gender=%s  WHERE id=%s" ,(name, email, phone, birthday, emergencyName, emergencyPhone, gender, member_id))
            connection_object.commit()
            print(mycursor.rowcount, "record inserted.")
            mycursor.close()
            connection_object.close()
            return make_response("更新成功",200)
        except Exception as e:
            # print(e)
            data={
                "error": True,
                "message":"伺服器錯誤"
            }
            json_result=jsonify(data)
            mycursor.close()
            connection_object.close()
            return json_result,500
    else:
        data={
                "error":True,
                "message":"請先登入會員"
            }
        # print(data)
        json_result=jsonify(data)
        return json_result,403
# 打開會員頁面時,顯示已經填入的訊息
@app.route("/api/member",methods=["GET"])
def getMember():
    cookie=request.cookies.get("Set-Cookie")
    if cookie != None:
        decode= jwt.decode(cookie, "secretJWT", ['HS256'])
        member_id=decode["id"]
        member_name=decode["name"]
        # 從前端接收資料
        
        connection_object = connection_pool.get_connection()
        mycursor = connection_object.cursor(dictionary=True)
        try:
            mycursor.execute("SELECT * FROM member WHERE id=%s",(member_id,))
            result = mycursor.fetchall()
            name=result[0]["name"]
            email=result[0]["email"]
            member_phone=result[0]["member_phone"]
            birthday=result[0]["birthday"]
            emergency_name=result[0]["emergency_name"]
            emergency_phone=result[0]["emergency_phone"]
            gender=result[0]["gender"]
            data={
                "name":name,
                "email":email,
                "member_phone":member_phone,
                "birthday":str(birthday),
                "emergency_name":emergency_name,
                "emergency_phone":emergency_phone,
                "gender":gender
            }
            json_result=jsonify(data)
            mycursor.close()
            connection_object.close()
            return make_response(json_result,200) 
        except Exception as e:
            # print(e)
            data={
                "error": True,
                "message":"伺服器錯誤"
            }
            json_result=jsonify(data)
            mycursor.close()
            connection_object.close()
            return json_result,500
    else:
        data={
                "error":True,
                "message":"請先登入會員"
            }
        # print(data)
        json_result=jsonify(data)
        return json_result,403
app.run(host="0.0.0.0",port=3000,debug=True)