from flask import Flask,Response,request, jsonify
import mysql.connector;
import json
# 连接数据库
db = mysql.connector.connect(
    host="localhost",
    user="dbuser",
    passwd="password",
    database="iems5722"
)
app = Flask(__name__)
# 开始事务
db.start_transaction()

# 获取游标对象: CMySQLCursor
cursor = db.cursor(dictionary=True)
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/api/a3/get_chatrooms', methods=['GET'])
def get_chatrooms():  # put application's code here
    cursor.execute("select * from chatrooms;")
    # data_classroom = cursor.fetchone()
    classrooms = cursor.fetchall()
    return_chatroom = {}
    data = []
    for classroom in classrooms:
        data.append(classroom)
    return_chatroom['data'] = data
    return_chatroom['status'] = "OK"
        # print(classroom)
    return Response(json.dumps(return_chatroom), mimetype='application/json')

@app.route('/api/a3/get_messages', methods=['GET'])
def get_messages():
    chatroom_id = request.args.get("chatroom_id")
    page = request.args.get("page")
    # cursor.execute("select * from messages ORDER BY id DESC LIMIT 5 OFFSET 0;")
    # date_format(message_time, '%Y-%m-%d %H:%i:%s')message_time
    cursor.execute("select message,name,date_format(message_time, '%Y-%m-%d %H:%i:%s') as message_time,user_id from messages WHERE chatroom_id="+chatroom_id+" ORDER BY id LIMIT 5 OFFSET "+page+";")
    messages = cursor.fetchall()
    print(messages)
    cursor.execute("SELECT COUNT(*) as total_pages FROM messages")
    total_pages = cursor.fetchall()
    data_tuple = {}
    datas = {}
    data_tuple['current_page'] = page;
    message_list = []
    for item in messages:
        message_list.append(item)
    data_tuple["messages"] = message_list
    data_tuple["total_pages"] = total_pages
    datas['data'] = data_tuple
    datas['status'] = "OK"
    return Response(json.dumps(datas), mimetype='application/json')

@app.route('/api/a3/send_message', methods=['POST'])
def send_message():
    return ''
# if __name__ == '__main__':
#     app.run()
if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5000',debug=True)