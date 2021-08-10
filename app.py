from flask import Flask, render_template, request
import boto3
app = Flask(__name__)
from werkzeug.utils import secure_filename

import pymysql
import pandas as pd
import csv
import os
import mysql.connector
import time


ACCESS_KEY='ASIAVFWPHPFGJCNMLP5O'
SECRET_KEY='+T+3ajEyY7mFNR2w6A7MfBGtX0mnfeeBnbqs8hzx'
SESSION_TOKEN='FwoGZXIvYXdzEI///////////wEaDMfnd04kCTpiYXG6LCK/Ae2dCBXpB+vp6mHjrucdhdkyl6Uno36qDfTw0pY4vdPWYSfOV6bjOUC+Ir9LAe5PYpSdjus08igS95OVY0fmQIK6asy8J1faTS3s6SYidPz/WsGYL0APEqaIqR1hHE/kskbwI7EJleZWGyUEY1a5bRSjm2CKXx0EXiGjLCZahzyqt6eA6vUO/xv0nXfXq6CHgg3GRGaw92Q1usVr+2QsZD+aDHNhDYIev7pPxCCskzPdhEYyRd89fQwEw44m4N7dKM2jwYgGMi051pMyL+SWOaUo5vJiokiKSM3kkVyamQFdh1qeW2OLiZiFcorI7e2tW2aNsd0='
users=[]

conn=pymysql.connect(
        host = 'database-1.ccojccy4dvmc.us-east-1.rds.amazonaws.com',
        user = 'admin',
        port = 3306,
        password = '12345678')

cursor1=conn.cursor()


s3 = boto3.client('s3',
                    aws_access_key_id=ACCESS_KEY,
                    aws_secret_access_key=SECRET_KEY,
                    aws_session_token = SESSION_TOKEN
                     )

BUCKET_NAME='pr365bucket'


#@app.route('/home') 
def home():
    return render_template("index.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':	
        us1 = request.form.get('emu1',False)
        p1 = request.form.get('psu1',False)

        print(us1)
        print(p1)

        

        sql= '''use UAB'''
        cursor1.execute(sql)
        cursor1.connection.commit()

        sql= '''insert into student(username,password) values ('%s','%s')'''%(us1,p1)
        a=cursor1.execute(sql)
        cursor1.connection.commit()

        #a=cursor1.fetchall()

        print(a)

        if a== 1:
            return render_template("login.html",msg1='successfully registered you can login now')
        else:
            return render_template("register.html",msg2='Select unique username')

    return render_template("register.html")

@app.route('/')
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        em1 = request.form.get('em1',False)
        ps1 = request.form.get('ps1',False)

        users.append(em1)

        print(em1)
        print(ps1)

        print(request.json)
        print(request.data)

        sql= '''use UAB'''
        cursor1.execute(sql)
        cursor1.connection.commit()

        sql='''select username from student where username = '%s' and password = '%s' '''%(em1,ps1)
        #sql='''select * from student'''
        #sql= '''show tables'''
        print(sql)
        cursor1.execute(sql)
        cursor1.connection.commit()
        
        useraccess=cursor1.fetchall()

        print(useraccess)

        if len(useraccess)>0:
            return render_template("index.html",msg=em1,m1='welcome '+em1)
        
        else:
            return render_template("login.html",msg1='You do not have access please register')

    return render_template("login.html")


@app.route('/upload',methods=['post'])
def upload():

    print(users)

    if request.method == 'POST':
        img = request.files['file']
        e1 = request.form.get('email1',False)
        e2 = request.form.get('email2',False)
        e3 = request.form.get('email3',False)
        e4 = request.form.get('email4',False)
        e5 = request.form.get('email5',False)
        some_list_of_contacts=[]
        some_list_of_contacts.append(e1)
        some_list_of_contacts.append(e2)
        some_list_of_contacts.append(e3)
        some_list_of_contacts.append(e4)
        some_list_of_contacts.append(e5)
        print(e1)
        print(e2)
        print(e3)
        print(e4)
        print(e5)

        #b=request.form.get('custId',False)
        c=users[-1]
        print(c)


        if img:
            filename = secure_filename(img.filename)
            print(filename)
            img.save(filename)
            s3.upload_file(Bucket = BUCKET_NAME,Filename=filename,Key = filename,ExtraArgs={'ACL': 'public-read'})
            msg = "Upload Done and email sent! "
        
    S3_LOCATION = 'https://{}.s3.amazonaws.com/'.format(BUCKET_NAME)
    S3_Final = "{}{}".format(S3_LOCATION, filename)
    print(S3_Final)
    
    client = boto3.client(
    "sns",
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    aws_session_token = SESSION_TOKEN,
    region_name="us-east-1"
    )

    
    topic = client.create_topic(Name="notifications")
    topic_arn = topic['TopicArn']
    
    print(len(some_list_of_contacts))
    print(some_list_of_contacts)
    count = 0
    for ele in some_list_of_contacts:
        if (ele != ''):
            count = count + 1
    
    if count>0:
        some_list_of_contacts = [i for i in some_list_of_contacts if i != '']
        
        for number in some_list_of_contacts:
            client.subscribe(
            TopicArn=topic_arn,
            Protocol='email',
            Endpoint=number,
            ReturnSubscriptionArn=True
            )

        client.publish(Message=S3_Final, TopicArn=topic_arn)

        sql= '''use UAB'''
        cursor1.execute(sql)
        cursor1.connection.commit()

        sql= '''insert into files(username,fileinfo) values ('%s','%s')'''%(c,filename)
        cursor1.execute(sql)
        cursor1.connection.commit()

        return render_template("index.html",m1=msg)
    
    else:
        return render_template("index.html",m1='Please enter valid email ids')

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)