# -*- coding:utf-8 -*-

import mysql.connector

# 打开数据库连接（请根据自己的用户名、密码及数据库名称进行修改）
cnn = mysql.connector.connect(
    host="localhost",
    user='root',
    passwd='1234',
)

mycursor = cnn.cursor()
mycursor.execute("SHOW DATABASES")
for x in mycursor:
    print(x)
