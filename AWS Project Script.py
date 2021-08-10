ACCESS_KEY='ASIAVFWPHPFGNMKAQ7SU'
SECRET_KEY='vzN0KzH6ZOjb/89QbaxKWhNc7Bbu1O43evN3djAH'
SESSION_TOKEN='FwoGZXIvYXdzEEsaDBjwdxy8S7rbyOTTvSK/AXFad9lmL1QfMu4TO5u7Xh3kla9HB3PiFr+3nxTtHCDyAe2nG66GNELGs87+bgJnrLj1wWW54R/9AgjPDVEH9elHOfJa0KEqrXT6EJ40HpCA6mwheyySRZlJ23CYUlmzxZqKEVZvgP3hSjf6kwIOeB9koIlMgDA8y75NitSm5oTn0/CnxbThkKh1ieIkQyNSkCLW54gXYi0nysJVLCX+7E1mqC/P7wTwGlpJtd5jQgGCvVLgyiI9/H/lSjgzdV0bKJqqsogGMi0DZ1j9FyA/0CEuy9k3Muzf+yl1Irr7M7VmP44amSTLM0sjZJUT1DiE8PuVNi8='


import pymysql
import pandas as pd
import csv
import os
import mysql.connector
import time
import boto3


conn=pymysql.connect(
        host = 'database-1.ccojccy4dvmc.us-east-1.rds.amazonaws.com',
        user = 'admin',
        password = '12345678')
cursor=conn.cursor()
cursor.execute("select version()")
data=cursor.fetchone()


sql= '''create database UAB'''
cursor.execute(sql)
cursor.connection.commit()



sql= '''use UAB'''
cursor.execute(sql)

sql= '''
create table student(
username varchar (20) ,
password text,
primary key(username)
)
'''
cursor.execute(sql)


sql= '''
create table files(
username varchar (20),
fileinfo text
)
'''
cursor.execute(sql)

some_list_of_contacts=['praneethreddy365@gmail.com','soddumpraneethreddy95@gmail.com','pranith@uab.edu','psoddum@gmail.com','praneethsoddum5@gmail.com']


client = boto3.client(
    "sns",
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    aws_session_token = SESSION_TOKEN,
    region_name="us-east-1"
    )

    
    topic = client.create_topic(Name="notifications")
    topic_arn = topic['TopicArn']  # get its Amazon Resource Name

    for number in some_list_of_contacts:

        client.subscribe(
        TopicArn=topic_arn,
        Protocol='email',
        Endpoint=number,
        ReturnSubscriptionArn=True
        )    
