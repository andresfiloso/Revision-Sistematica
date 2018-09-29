#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, json, session, url_for, jsonify

from app import app
import MySQLdb
from bs4 import BeautifulSoup
import requests
import time

app = Flask(__name__,
			instance_relative_config=True,
			template_folder='templates')


# Ir al workbench y en "users and privileges" probar alguno que ande
# la mayori tienden a no andar, yo la emboque no se como
# La DB y la tabla las cree en el workbench, no se como hacerlo desde aca (todavia..)

db = MySQLdb.connect(host="127.0.0.1",
					 user="root",
					 passwd="",
					 db="rsdb")



cur = db.cursor()
conf=False

cur2 = db.cursor()

@app.route('/')
def default():
	return redirect(url_for('home'),code=307)


@app.route('/home',methods = ['POST', 'GET'])
def home():
	return render_template('login.html')

@app.route('/login',methods = ['POST', 'GET'])
def login():
	if request.method == 'POST':
		user = request.form["user"] #Recibo User desde el form
		password = str(request.form["pass"]) #Recibo Pass desde el form

		rows = cur.execute("SELECT * FROM Usuario where usuario = '" + user + "' and pass = '" + password + "'")

		for r in cur.fetchall():

			datosUsuario = {
				'idUsuario' : r[0],
				'usuario' : r[1],
				'email' : r[3]
			}

		if rows == 1: #Autenticacion correcta

			proyectosArray = {}
			proyectos_ready = {}

			session['datosUsuario'] = datosUsuario # Se guardan los datos del usuario en la session.

			cur2.execute("SELECT * FROM Proyecto where idUsuario = " + str(datosUsuario['idUsuario']))

			i = 0
			for r in cur2.fetchall():

				print "id:" + str(r[0])
				print "nombre:" + str(r[1])
				print "descr:" + str(r[2])
				print "inclu:" + str(r[3])
				print "exclu:" + str(r[4])

				proyecto = {
				'idProyecto' : r[0],
				'proyecto' : r[1],
				'descripcion' : r[2],
				'inclusion': r[3],
				'exclusion': r[4]
				}

				proyectosArray[i] = proyecto
				i = i + 1

			print "Cantidad de proyectos encontrados: "
			print i
			proyectos_ready = json.dumps(proyectosArray)
			session['proyectos'] = proyectosArray

			print "Welcome " + user
			return render_template('projects.html')
		else:
			error = 'Usuario o clave incorrecta!'
			print error
			return render_template('login.html', error = error)

@app.route('/lookup',methods = ['POST', 'GET'])
def lookup():

	return render_template('lookup.html',) 

@app.route('/scrapping',methods = ['POST', 'GET'])
def scrapping():
	print "PARAMETROS GET: " #Prueba que no funciono. Aca hay que tomar los datos del input keywords y meterlos en la url
	print request.args.get("urlParams%5Bkeywords%5D%5B%5D") #Prueba que no funciono
	urlScience = "https://www.sciencedirect.com/search?qs=" + "software" + "&show=10&sortBy=relevance"
	print urlScience
	req = requests.get(urlScience)
	statusCode = req.status_code
	html = BeautifulSoup(req.text, "html.parser")
	rawScience = html.findAll('div', {'class': 'result-item-content'})

	data_ready = {}

	dataArray = {}

	i = 0

	for link in rawScience:

		if(i < 5):
			result = "https://www.sciencedirect.com" + link.a['href']

			req = requests.get(result)
			statusCode = req.status_code
			html = BeautifulSoup(req.text, "html.parser")
			title = html.find('span', {'class': 'title-text'}).text
			abstract = html.find('div', {'class': 'abstract author'}).text

			data = {
				'id' : i,
				'title' : title,
				'result' : result,
				'abstract' : abstract
			}

			print title.encode('utf8')
			print result.encode('utf8')
			print abstract.encode('utf8')

			dataArray[i] = data

			i = i+1

	print "AAAAAAAAAAAAAAAAAAa"
	print "Cantidad de articulos"
	print i

	session['cantArticulos'] = i
	#session['articulos'] = dataArray
	data_ready = json.dumps(dataArray)

	return data_ready

	#return render_template('results.html',data_ready=json.loads(data_ready))



@app.route('/results',methods = ['POST', 'GET'])
def results():
	return render_template('results.html')


@app.route('/article',methods = ['POST', 'GET'])
def article():
	title = request.args.get("title")
	session['titulo'] = title
	url = request.args.get("url")
	session['link'] = url

	abstract = request.args.get("abstract")

	session['abstract'] = abstract

	return render_template('article.html')


@app.route('/projects',methods = ['POST', 'GET'])
def projects():
	return render_template('projects.html')

@app.route('/newProyect',methods = ['POST', 'GET'])
def newProyect():
	return render_template('newProyect.html')


@app.route('/classify',methods = ['POST', 'GET'])
def classify():
	return render_template('classify.html')

