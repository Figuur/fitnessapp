from flask import Flask
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
import mysql.connector

mydb = mysql.connector.connect(
  host="raimondappdb.mysql.database.azure.com",  #port erbij indien mac
  user="raimondadmin",
  password="uiop7890UIOP&*()",
  database="lutsendb"
)

@app.route("/testkort")
def oefeningen():
    return "halter benchpress"

@app.route("/bench_oefeningen")
def alleoefeningen():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM bench_oefeningen")
    myresult = mycursor.fetchall()
    keys = [i[0] for i in mycursor.description]
    data = [
        dict(zip(keys, row)) for row in myresult
    ]
    return data