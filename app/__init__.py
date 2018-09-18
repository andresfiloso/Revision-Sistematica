#!/usr/bin/python
from flask import Flask, render_template, request, redirect, json, session, url_for
from app import app
import MySQLdb
from bs4 import BeautifulSoup
import requests

app = Flask(__name__,
            instance_relative_config=True,
            template_folder='templates')


# Ir al workbench y en "users and privileges" probar alguno que ande
# la mayori tienden a no andar, yo la emboque no se como
# La DB y la tabla las cree en el workbench, no se como hacerlo desde aca (todavia..)

db = MySQLdb.connect(host="127.0.0.1",
                     user="root",
                     passwd="",
                     db="usuario")



cur = db.cursor()
conf=False

@app.route('/')
def default():
	return redirect(url_for('home'),code=307)


@app.route('/home',methods = ['POST', 'GET'])
def home():
    return render_template('login.html')

@app.route('/login',methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        result = request.form       #usar request.form porque request.get_json() no funciona
        usr = request.form["user"]
        passwd = str(request.form["pass"])

        rows = cur.execute("SELECT * FROM usuarios where nombre = '"+usr+"' and pass = '"+passwd+"'")

        if rows == 1:
        	messages = json.dumps({"user":usr,"pass":passwd})
        	session['messages'] = messages
        	return redirect(url_for('lookup'),code=307)
        else:
        	return redirect(url_for('home'),code=307)

@app.route('/lookup',methods = ['POST', 'GET'])
def lookup():

	messages = session['messages']

	return render_template('lookup.html',messages=json.loads(messages))

@app.route('/scrapping',methods = ['POST', 'GET'])
def scrapping():
	if request.method == "POST":
		arg = request.form["arg"]

	urlScience = "https://www.sciencedirect.com/search?qs=" + arg + "&show=10&sortBy=relevance"
	req = requests.get(urlScience)
	statusCode = req.status_code
	html = BeautifulSoup(req.text, "html.parser")
	rawScience = html.findAll('div', {'class': 'result-item-content'})
	data_ready = {}

	dataArray = {}

	i = 0

	for link in rawScience:
	    result = "https://www.sciencedirect.com" + link.a['href']

	    data = {
	    	'title' : 'title',
	    	'result' : result,
	    	'abstract' : 'abstract'
	    }

	    dataArray[i] = data

	    i = i+1

	print "AAAAAAAAAAAAAAAAAAa"
	print i

	data_ready = json.dumps(dataArray)
	#session['data_ready'] = data_ready


	return data_ready

	#return render_template('results.html',data_ready=json.loads(data_ready))


@app.route('/results',methods = ['POST', 'GET'])
def results():
	return render_template('results.html')
