import json
from flask import jsonify
import mysql.connector
from mysql.connector.pooling import MySQLConnectionPool
from mySQL import MySQLPassword
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
from flask import jsonify 
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
                print(photo_str)
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
        #     print(type(category[0]))
        # print(category_result)
        
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


app.run(host="0.0.0.0",port=3000,debug=True)