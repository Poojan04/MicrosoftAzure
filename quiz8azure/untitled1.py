from flask import Flask,render_template,request
from os import listdir
from azure.storage.blob import ContentSettings
from azure.storage.blob import BlockBlobService
import pyodbc
import os,os.path
from os.path import isfile, join
import csv
import time
import random
import sys
app = Flask(__name__)
server = 'quizazure8.database.windows.net'
database = 'sqldbquiz'
username = 'rootpooja'
password = 'Pooja@narayan4'
driver= '{SQL Server}'
db = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = db.cursor()
            #db = pyodbc.connect(user="rootpooja@mysqlquiz8", password="Pooja@narayan4", host="quizazure8.database.windows.net",
             #                  port=3306, database="test",local_infile=True,charset='utf8mb4',DRIVER='{ODBC Driver 13 for SQL Server}')
print("connected")



@app.route('/')
def hello_world():
    return render_template('dbview.html')

@app.route('/viewtab',methods=['GET','POST'])
def createtable():
    cursor = db.cursor()
    cursor.execute('DROP TABLE IF EXISTS FoodData;')
    cursor.commit()
    cursor.execute("CREATE TABLE FoodData(filename varchar(30), quantity varchar(25),ingredients varchar(175),cusine varchar(20));")
    cursor.commit()
    csvfiles = os.listdir("C:\\Users\\Pooja\\Desktop\\csv")
    print (csvfiles)
    for file in csvfiles:
        filename = os.path.splitext(file)[0]
        with open("C:\\Users\\Pooja\\Desktop\\csv\\"+filename+".csv") as f:
            print (filename)
            for i,line in enumerate(f):
                if i==0:
                    quantity = line.rstrip(",\n")
                    #print (quantity)
                if i==1:
                    ingredients = line.rstrip(",\n")
                    #print (ingredients)
                if i==2:
                    cusine = line.rstrip(",\n")
                    #print (cusine)             
         
        cursor.execute('INSERT INTO FoodData (filename,quantity,ingredients,cusine) values (\''+filename+'\',\''+quantity+'\',\''+ingredients+'\',\''+cusine+'\');')
        cursor.commit()
        
    return "created"
@app.route('/querydatabase' ,methods=['POST', 'GET'])
def querydatabase() :
    beforeTime = time.time()
    print (beforeTime)
    cursor = db.cursor()
    param = 'wheat'
    #p1=(100)
    #p2=(500)
    cursor.execute('SELECT * FROM FoodData where ingredients like \'%'+param+'%\';')
    #cursor.execute('SELECT * FROM FoodData where quantity between '+int(p1)+' and '+int(p1)+';')

    result = cursor.fetchall()
    print ("Count is " + str(result))
    afterTime = time.time()
    print (afterTime)
    timeDifference = afterTime - beforeTime
    print (timeDifference)

    return render_template('index.html', tableData=result)

port = os.getenv('PORT', '8080')
if __name__ == '__main__':
    # app.run()
    app.run(host='0.0.0.0', port=int(port))
