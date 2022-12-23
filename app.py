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
connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    user='root',
    password=MySQLPassword(),
    host='127.0.0.1',
    database='taipei_trip',
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
                # print(lng)
                # 圖片處理
                mycursor.execute("SELECT group_concat(photo) FROM attraction INNER JOIN photo ON attraction.id=photo.photo_id WHERE attraction.id=%s group by photo.photo_id" ,(id,))
                photo = mycursor.fetchone()
                # print(photo)
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
        # print(data)
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
    # print(attraction)
    # print(date)
    # print(time)
    # print(price)
    # 一定要先登入,先檢查是否有登入
    cookie=request.cookies.get("Set-Cookie")
    print(cookie)
    if cookie != None:
        decode= jwt.decode(cookie, "secretJWT", ['HS256'])
        member_id=decode["id"]
        member_name=decode["name"]
        # print(decode,"20221216")
        # print(decode["id"])
        # print(decode["name"])
        
        # 每個資料都不能為空
        if time=="" or date=="":
            data={
                "error":True,
                "message":"請選擇日期和時間"
            }
            # print(data)
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
    else:
        data={
                "error":True,
                "message":"請先登入會員"
            }
        # print(data)
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
        # 有使用者id就可以找出他的reservation資料
        # mycursor.execute('SELECT * FROM reservation WHERE member_id=%s' ,(member_id,))
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

                # print(result)
                # print(attraction_id)
                # print(attraction_name)
                # print(attraction_address)
                # print(reservation_id)
                # print(date)
                # print(time)
                # print(price)
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
    print(cookie)
    if cookie != None:
        decode= jwt.decode(cookie, "secretJWT", ['HS256'])
        member_id=decode["id"]
        member_name=decode["name"]
        # 從前端接收資料
        ab=request.json
        print(ab)
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

                print(price)
            except:
                data={
                    "error": True,
                    "message":"伺服器錯誤"
                }
                json_result=jsonify(data)
                mycursor.close()
                connection_object.close()
                return json_result,500
        print(prime)
        print(total_price)
        print(name)
        print(phone)
        print(reservationNum,"len")
        print(reservation_id)
        
        # 然後進入tappay api
        mydata={
            "prime":prime,
            "partner_key": "partner_r3zqFU0dKDS6gH6n5SzwYHgEmft52ib29bZiDkNup207HiKBMPm0TpDf",
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
            "x-api-key": "partner_r3zqFU0dKDS6gH6n5SzwYHgEmft52ib29bZiDkNup207HiKBMPm0TpDf",
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
    connection_object = connection_pool.get_connection()
    mycursor=connection_object.cursor()
    try:
        mycursor.execute("SELECT * FROM order_model WHERE order_number=%s",(orderNumber,))
        result = mycursor.fetchall()
        # print(type(result))
        if result != None:
            print(result)
           
            # attraction_list={
            #     "id":id ,
            #     "name":name,
            #     "category":category,
            #     "description":description,
            #     "address":address,
            #     "transport":transport,
            #     "mrt":mrt,
            #     "lat":lat,
            #     "lng":lng,
            #     "images":photo_str
            # }
            
            # data={
            #     "data":attraction_list
            # }
			
            # json_result=jsonify(data)
            # # print(json_result)
            # mycursor.close()
            # connection_object.close()
            # return json_result
            return "1111"
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


app.run(host="0.0.0.0",port=3000,debug=True)