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
	try:
		print "idUSuario"
		print session['datosUsuario']['idUsuario'] #Busco variable de session de login. Si no hay session, entra en el catch y redirige a home


		return redirect(url_for('projects'))
	except Exception as e:
		#error = "Session Timeout"
		return render_template('login.html',)

@app.route('/logout',methods = ['POST', 'GET'])
def logout():
	session.clear()
	return render_template('login.html')

@app.route('/login',methods = ['POST', 'GET'])
def login():
	if request.method == 'POST':
		user = request.form["user"] 
		password = str(request.form["pass"]) 

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
			return redirect(url_for('projects'))
		else:
			error = 'Usuario o clave incorrecta!'
			print error
			return render_template('login.html', error = error)


@app.route('/signup',methods = ['POST', 'GET'])
def signup():
	return render_template('register.html',) 


@app.route('/lookup',methods = ['POST', 'GET'])
def lookup():
	try:
		print "idUSuario"
		print session['datosUsuario']['idUsuario'] #Busco variable de session de login. Si no hay session, entra en el catch y redirige a home


		return render_template('lookup.html',) 
	except Exception as e:
		return redirect(url_for('home'))


@app.route('/micuenta',methods = ['POST', 'GET'])
def micuenta():
	try:
		print "idUSuario"
		print session['datosUsuario']['idUsuario'] #Busco variable de session de login. Si no hay session, entra en el catch y redirige a home


		return render_template('micuenta.html',) 
	except Exception as e:
		return redirect(url_for('home'))

@app.route('/results',methods = ['POST', 'GET'])
def results():
	try:
		print "idUSuario"
		print session['datosUsuario']['idUsuario'] #Busco variable de session de login. Si no hay session, entra en el catch y redirige a home

		keywords = request.args.get('keywords', default = '*', type = str)
 		newKeyword = request.args.get('newKeyword', default = '*', type = str)

 		session['keywords'] = keywords

		return render_template('results.html', keywords = keywords)
	except Exception as e:
		return redirect(url_for('home'))


@app.route('/scrapping',methods = ['POST', 'GET'])
def scrapping():
	print "PARAMETROS GET: "
	print session['keywords']
	args = session['keywords'].replace('; ', ' AND ')
	print "Argumentos a pasar a la query: " + str(args)
	session['query'] = args

	urlScience = "https://www.sciencedirect.com/search?qs=" + args + "&show=10&sortBy=relevance"
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
			print result
			req = requests.get(result)
			statusCode = req.status_code
			html = BeautifulSoup(req.text, "html.parser")
			title = html.find('span', {'class': 'title-text'})
			if(title != None):
				title = title.text
			else:
				title = "El articulo no tiene titulo"
			abstract = html.find('div', {'class': 'abstract author'})
			if(abstract != None):
				abstract = abstract.text
			else:
				abstract = "El articulo no tiene abstract"
			keywords = html.find('div', {'class': 'keywords-section'})
			if(keywords != None):
				keywords = keywords.text
			else:
				keywords = "El articulo no tiene palabras claves"

			data = {
				'id' : i,
				'title' : title,
				'result' : result,
				'abstract' : abstract,
				'keywords' : keywords
			}

			print title.encode('utf8')
			print result.encode('utf8')
			print abstract.encode('utf8')
			print keywords.encode('utf8')

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



@app.route('/article',methods = ['POST', 'GET'])
def article():
	try:
		print "idUSuario"
		idUsuario = session['datosUsuario']['idUsuario'] #Busco variable de session de login. Si no hay session, entra en el catch y redirige a home
		print idUsuario

		title = request.form["titulo"]
		print title
		url = request.form["url"]
		print url
		abstract = request.form["abstract"]
		print abstract.encode('utf-8')
		keywords = request.form["keywords"]
		print keywords.encode('utf-8')

		#abstract =  rawAbstract.replace('Abstract', '<h2 class="card-title">Abstract</h2>')

		article = {
				'title': title,
				'url': url,
				'abstract': abstract,
				'keywords': keywords
			}

		print "SE VA A CARGAR ARTICULO EN SESION"
		session['article'] = article
		print "ARTICULO CARGADO EN SESSION"
		return render_template('article.html')
	except Exception as e:
		print "Type error: " + str(e)
		return redirect(url_for('home'))
	


@app.route('/projects',methods = ['POST', 'GET'])
def projects():
	try:
		print "idUSuario"
		print session['datosUsuario']['idUsuario'] #Busco variable de session de login. Si no hay session, entra en el catch y redirige a home

		return render_template('projects.html')
	except Exception as e:
		return redirect(url_for('home'))


@app.route('/newProyect',methods = ['POST', 'GET'])
def newProyect():
	try:
		print "idUSuario"
		idUsuario = session['datosUsuario']['idUsuario'] #Busco variable de session de login. Si no hay session, entra en el catch y redirige a home
		print idUsuario

		return render_template('newProyect.html')
	except Exception as e:
		return redirect(url_for('home'))

@app.route('/insertProyecto',methods = ['POST', 'GET'])
def insertProyecto():
	if request.method == 'POST':

		print "idUSuario"
		idUsuario = session['datosUsuario']['idUsuario']
		print idUsuario

		nombre = request.form["nombre"]
		print nombre
		descripcion = request.form["descripcion"]
		print descripcion
		inclusion = request.form['inclusion']
		print inclusion
		exclusion = request.form['exclusion']
		print exclusion

		sql = "INSERT INTO `Proyecto` (`proyecto`, `descripcion`, `inclusion`, `exclusion`, `idUsuario`) VALUES ('" + nombre + "', '" + descripcion + "', '" + inclusion + "', '" + exclusion + "', '" + str(idUsuario) + "')"

		print sql

		rows = cur.execute(sql)

		print "ROWSSSSS"
		print rows
		proyectosArray = {}

		cur2.execute("SELECT * FROM Proyecto where idUsuario = " + str(idUsuario))

		i = 0
		for r in cur2.fetchall():
			print "id:" + str(r[0])
			print "nombre:" + str(r[1])
			print "descr:" + str(r[2])
			print "inclu:" + str(r[3])
			print "exclu:" + str(r[4])

			proyecto = {
				'idProyecto': r[0],
				'proyecto': r[1],
				'descripcion': r[2],
				'inclusion': r[3],
				'exclusion': r[4]
			}

			proyectosArray[i] = proyecto
			i = i + 1

		print "Cantidad de proyectos encontrados: "
		print i
		session['proyectos'] = proyectosArray
		session['status'] = "Proyecto creado correctamente"

	return redirect(url_for('projects'))

@app.route('/classify',methods = ['POST', 'GET'])
def classify():
	try:
		print "idUSuario"
		print session['datosUsuario']['idUsuario'] #Busco variable de session de login. Si no hay session, entra en el catch y redirige a home

		idProyecto = request.args.get('project-id')
		print "IDPROYECTO: " + str(idProyecto)

		cur2.execute("SELECT * FROM Proyecto where idProyecto = " + str(idProyecto))

		proyectoActual = {}
		i = 0
		for r in cur2.fetchall():
			print "id:" + str(r[0])
			print "nombre:" + str(r[1])
			print "descr:" + str(r[2])
			print "inclu:" + str(r[3])
			print "exclu:" + str(r[4])

			proyecto = {
				'idProyecto': r[0],
				'proyecto': r[1],
				'descripcion': r[2],
				'inclusion': r[3],
				'exclusion': r[4]
			}

			proyecto
			i = i + 1

		print "Cantidad de proyectos encontrados: DEBERIA SER UNO -> " + str(i)
		session['proyecto'] = proyecto

		return render_template('classify.html')
	except Exception as e:
		return redirect(url_for('home'))
	

