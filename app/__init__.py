#!/usr/bin/python
from flask import Flask, render_template, request
from app import app
import MySQLdb

app = Flask(__name__,
            instance_relative_config=True,
            template_folder='templates')


# Ir al workbench y en "users and privileges" probar alguno que ande
# la mayori tienden a no andar, yo la emboque no se como
# La DB y la tabla las cree en el workbench, no se como hacerlo desde aca (todavia..)

db = MySQLdb.connect(host="127.0.0.1",
                     user="root",
                     passwd="225588Aa",
                     db="usuario")



cur = db.cursor()
conf=False

@app.route('/')
def home():
    return render_template('login.html')


@app.route('/login',methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        result = request.form       #usar request.form porque request.get_json() no funciona
        usr = request.form["user"]
        passwd = request.form["pass"]
        print "Valores: "
        print usr
        print passwd
        for key,value in result.iteritems():        #result contiene un diccionario con los valores
            print  key +" "+ value #Imprime el campo y value, que  es lo que tenemos que extraer!!

	    cur.execute("SELECT nombre,passwd FROM usuarios")
	    rows = cur.fetchall()
	    for row in rows:
	        for col in row:
	            print "%s," % col
	        print "\n"



    return  render_template("lookup.html",result = result) #para que despues lo mande al otro .html