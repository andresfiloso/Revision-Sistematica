# -*- coding: utf-8 -*-
from flask import session, jsonify, json
from datasource import *
from models import *
import datetime

datasource = DataSource()

#####################################################################
# DataSource es un objteo que permite el acceso a la base de datos.	#
# Informacion de esta clase en datasource.py 						#
#####################################################################

import sys
# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

def auth_user(user, password):
	cur = get_cur(datasource)

	sql = ("SELECT * FROM usuario where usuario = '" + user + "' and pass = '" + password + "'")
	rows = cur.execute(sql)

	for row in cur:
		usuario = Usuario(row['idUsuario'], row['usuario'], row['email'])
		session['usuario'] = usuario.getIdUsuario()
		return rows


def getSession():

	cur = get_cur(datasource)

	sql = ("SELECT * FROM Usuario where idUsuario = '" + str(session['usuario']) + "'")
	rows = cur.execute(sql)

	for row in cur:
		usuario = Usuario(row['idUsuario'], row['usuario'], row['email'])

	return usuario


def get_user(idUsuario):
	cur = get_cur(datasource)

	sql = ("SELECT * FROM Usuario where idUsuario = '" + str(idUsuario) + "'")
	rows = cur.execute(sql)

	for row in cur:
		usuario = row['usuario']

	return usuario

def get_all_users():
	cur = get_cur(datasource)
	sql = ("SELECT * FROM Usuario")
	rows = cur.execute(sql)

	usuarios = []

	i = 0
	for row in cur.fetchall():

		usuario = row['usuario']
		usuarios.append(usuario)

	return usuarios

def signup_user(usuario, email, password, password2):

	cur = get_cur(datasource)

	sql = ("SELECT count(*) FROM Usuario where usuario = '" + usuario + "'")
	rows = cur.execute(sql).fetchall()[0][0]

	print rows

	if rows != 0:
		print usuario + " was founded"
		session['error_desc'] = "El nombre de usuario ya esta en uso"
		return 0

	sql = ("SELECT count(*) FROM Usuario where email = '" + email + "'")
	rows = cur.execute(sql).fetchall()[0][0]

	if rows != 0:
		print email + " was founded"
		session['error_desc'] = "El email ya esta en uso"
		return 0

	if rows == 0:
		sql = ("INSERT INTO `usuario` (`idUsuario`, `usuario`, `pass`, `email`) VALUES (NULL, '"+usuario+"', '"+password+"', '"+email+"');")
		rows = get_cur(datasource).execute(sql)
		get_db(datasource).commit()
		print "Se dio de alta el usuario " + usuario
		return rows

def insert_colaboracion(usuario):

	cur = get_cur(datasource)

	sql = ("SELECT * FROM Usuario where usuario = '" + usuario + "'")
	rows = cur.execute(sql)

	idUsuario = ""

	for row in cur:
		idUsuario = row['idUsuario']

	sql = ("INSERT INTO `colaborador` (`idProyecto`, `idUsuario`) VALUES ('"+ str(session['proyecto']) +"', '"+str(idUsuario)+"');")
	rows = get_cur(datasource).execute(sql)
	get_db(datasource).commit()

	return rows



def get_projects():
	proyectos = {}

	# Proyectos donde se es autor
	cur = get_cur(datasource)
	sql = ("SELECT * FROM Proyecto where idUsuario = " + str(session['usuario']))
	rows = cur.execute(sql)

	i = 0

	for row in cur.fetchall():

		objetoProyecto = Proyecto(row['idProyecto'], row['proyecto'], row['descripcion'], row['inclusion'], row['exclusion'], get_user(row['idUsuario']))
		print objetoProyecto
		proyectos[i] = objetoProyecto
		i += 1

	# Proyectos donde se es colaborador
	sql = ("SELECT p.* FROM proyecto p inner join colaborador c where c.idUsuario = " + str(session['usuario']) + " and c.idProyecto = p.idProyecto")
	rows = cur.execute(sql)	


	for row in cur.fetchall():

		objetoProyecto = Proyecto(row['idProyecto'], row['proyecto'], row['descripcion'], row['inclusion'], row['exclusion'], get_user(row['idUsuario']))
		print objetoProyecto
		proyectos[i] = objetoProyecto
		i += 1


	return proyectos

def get_project(*args): # sobrecarga de metodo
	if len(args) == 0: # no arguments given
		cur = get_cur(datasource)
		sql = ("SELECT * FROM Proyecto where idProyecto = " + str(session['proyecto']))
		rows = cur.execute(sql)

		for row in cur:
			objetoProyecto = Proyecto(row['idProyecto'], row['proyecto'], row['descripcion'], row['inclusion'], row['exclusion'], get_user(row['idUsuario']))

		return objetoProyecto

	if len(args) == 1:
		cur = get_cur(datasource)
		sql = ("SELECT * FROM Proyecto where idProyecto = " + args[0])
		rows = cur.execute(sql)

		for row in cur:
			objetoProyecto = Proyecto(row['idProyecto'], row['proyecto'], row['descripcion'], row['inclusion'], row['exclusion'], get_user(row['idUsuario']))
			session['proyecto'] = objetoProyecto.getIdProyecto()
			return objetoProyecto

	if len(args) == 2:
		if(args[1] == False): # Bussiness rule. No seleccionar proyecto
			cur = get_cur(datasource)
			sql = ("SELECT * FROM Proyecto where idProyecto = " + args[0])
			rows = cur.execute(sql)

			for row in cur:
				objetoProyecto = Proyecto(row['idProyecto'], row['proyecto'], row['descripcion'], row['inclusion'], row['exclusion'], get_user(row['idUsuario']))
				return objetoProyecto

def get_articles():
	cur = get_cur(datasource)
	sql = ("SELECT * FROM Articulo where idProyecto = " + str(session['proyecto']))
	rows = cur.execute(sql)

	articulos = {}

	i = 0
	for row in cur.fetchall():
		
		articulo = Articulo(row['idArticulo'], row['articulo'], row['url'], row['test'], row['clasificacion'], row['keywords'], get_project().getProyecto(), get_user(row['idUsuario']))

		articulos[i] = articulo
		i +=1

	return articulos


def getVariablesArticles(articulos):
	cantidadClasificados = 0
	cantidadTesteados = 0
	for key in articulos:
		print articulos[key].getClasificacion()
		if (articulos[key].getClasificacion() != "0"):
			cantidadClasificados += 1
			print "Clasificados hasta ahora: " + str(cantidadClasificados)
		if (articulos[key].getTest()):
			cantidadTesteados += 1

	session["cantidadClasificados"]  = cantidadClasificados
	session["cantidadTesteados"] = cantidadTesteados

	return "0"

def get_article(idArticulo):
	cur = get_cur(datasource)

	sql = ("SELECT * FROM Article where idArticulo = '" + str(idArticulo) + "'")
	rows = cur.execute(sql)

	for row in cur:
		articulo = Articulo(row['idArticulo'], row['articulo'], row['url'], row['test'], row['clasificacion'], row['keywords'], get_project().getProyecto(), get_user(row['idUsuario']))

	return articulo


def classify_article(idArticulo, clasificacion):
	idUsuario = str(session['usuario'])
	sql = ("UPDATE `articulo` SET `clasificacion` = '" + clasificacion + "' WHERE `articulo`.`idArticulo` = " + str(idArticulo) + ";")
	rows = get_cur(datasource).execute(sql)
	get_db(datasource).commit()

	return rows

def get_transacciones():
	cur = get_cur(datasource)
	sql = ("SELECT * FROM Transaccion where idProyecto = " + str(session['proyecto']))
	rows = cur.execute(sql)

	transacciones = {}

	i = 0
	for row in cur.fetchall():
		transaccion = Transaccion(row['idTransaccion'], row['transaccion'], row['tipoTransaccion'], row['fechahora'], get_project().getProyecto(), get_user(row['idUsuario']))

		transacciones[i] = transaccion
		i +=1

	return transacciones


def get_busquedas():
	cur = get_cur(datasource)
	sql = ("SELECT * FROM Busqueda where idProyecto = " + str(session['proyecto']))
	rows = cur.execute(sql)

	busquedas = {}

	i = 0
	for row in cur.fetchall():

		busqueda = Busqueda(row['idBusqueda'], row['busqueda'], row['fechahora'], get_project().getProyecto(), get_user(row['idUsuario']))

		busquedas[i] = busqueda
		i +=1

	return busquedas


def get_colaboradores():
	cur = get_cur(datasource)
	sql = ("SELECT u.* FROM usuario u inner join colaborador c WHERE c.idProyecto =" + str(session['proyecto']) + " and c.idUsuario = u.idUsuario")
	print "SQL A EJECUTAR: " + sql
	rows = cur.execute(sql)

	colaboradores = {}

	i = 0
	for row in cur.fetchall():

		colaborador = Usuario(row['idUsuario'], row['usuario'], row['email'])
		print "COLABORADOR ENCONTRADO: " + str(colaborador)
		colaboradores[i] = colaborador
		i +=1

	return colaboradores

def new_busqueda(query):
	usuario = getSession()

	now = datetime.datetime.now()
	fechahora = now.strftime("%Y-%m-%d %H:%M")

	sql = ("INSERT INTO `busqueda` (`busqueda`, `fechahora`, `idProyecto`, `idUsuario`) VALUES ('" + query + "', '" + str(fechahora) + "', '"+str(session['proyecto'])+"', '"+str(usuario.getIdUsuario())+"');")
	rows = get_cur(datasource).execute(sql)
	get_db(datasource).commit()


def add_article(title, url, test):
	usuario = getSession()

	sql = ("INSERT INTO `articulo` ( `articulo`, `url`, `test`, `clasificacion`, `keywords`, `idProyecto`, `idUsuario`) VALUES ('" + title + "', '" + url + "', '" + test + "', '0', '" + session['keywords'] + "', '"+str(session['proyecto'])+"', '"+str(usuario.getIdUsuario())+"');")
	rows = get_cur(datasource).execute(sql)
	get_db(datasource).commit()

	return rows

def update_user(usuario, email):
	idUsuario = str(session['usuario'])
	sql = ("UPDATE `usuario` SET `usuario` = '" + usuario + "', `email` = '" + email + "' WHERE `usuario`.`idUsuario` = '" + idUsuario + "';")
	rows = get_cur(datasource).execute(sql)
	get_db(datasource).commit()

	usuario = {
		'idUsuario' : idUsuario,
		'usuario' : usuario,
		'email' : email
	}
	usuario = usuario
	return rows

def update_clasificacion(idArticulo, clasificacion):
	sql = ("UPDATE `articulo` SET `clasificacion` = '"+clasificacion+"' WHERE `articulo`.`idArticulo` = "+str(idArticulo)+";")
	rows = get_cur(datasource).execute(sql)
	get_db(datasource).commit()

	return rows

def update_project(idProyecto, proyecto, descripcion, inclusion, exclusion):

	proyectoAnterior = get_project(idProyecto, False)

	proyecto = proyecto.replace("'", "''")
	descripcion = descripcion.replace("'", "''")
	inclusion = inclusion.replace("'", "''")
	exclusion = exclusion.replace("'", "''")

	idUsuario = str(session['usuario'])
	sql = ("UPDATE `proyecto` SET `proyecto` = '" + proyecto + "', `descripcion` = '" + descripcion + "', `inclusion` = '" + inclusion + "', `exclusion` = '" + exclusion + "' WHERE `proyecto`.`idProyecto` = '" + idProyecto + "';")
	rows = get_cur(datasource).executescript(sql)
	get_db(datasource).commit()

	usuario = getSession()
	"""
	transaccion = usuario.getUsuario() + " edito el proyecto " + proyectoAnterior.getProyecto()
	now = datetime.datetime.now()
	fechahora = now.strftime("%Y-%m-%d %H:%M")

	sql = ("INSERT INTO `transaccion` (`transaccion`, `tipoTransaccion`, `fechahora`, `idProyecto`, `idUsuario`) VALUES ('" + transaccion + "', 'updateProject', '" + str(fechahora) + "', '"+str(idProyecto)+"', '"+str(usuario.getIdUsuario())+"');")
	rows = get_cur(datasource).execute(sql)
	get_db(datasource).commit()
	
	"""
	return rows

def delete_project(idProyecto):
	sql = ("DELETE FROM `proyecto` WHERE `proyecto`.`idProyecto` = '" + idProyecto + "';")
	rows = get_cur(datasource).execute(sql)
	get_db(datasource).commit()
	return rows

def delete_transaccion(idTransaccion):
	sql = ("DELETE FROM `transaccion` WHERE `transaccion`.`idTransaccion` = '" + idTransaccion + "';")
	rows = get_cur(datasource).execute(sql)
	get_db(datasource).commit()
	return rows

def new_proyect(nombre, descripcion, inclusion, exclusion):
	idUsuario = str(session['usuario'])
	sql = ("INSERT INTO `Proyecto` (`proyecto`, `descripcion`, `inclusion`, `exclusion`, `idUsuario`) VALUES ('" + nombre + "', '" + descripcion + "', '" + inclusion + "', '" + exclusion + "', '" + idUsuario + "')")
	rows = get_cur(datasource).execute(sql)
	get_db(datasource).commit()

	usuario = getSession()

	transaccion = usuario.getUsuario() + " creo el proyecto " + nombre
	now = datetime.datetime.now()
	fechahora = now.strftime("%Y-%m-%d %H:%M")

	sql = "SELECT MAX(idProyecto) FROM Proyecto" #Se va a buscar el ultimo id insertado
	cur = get_cur(datasource)
	rows = cur.execute(sql)
	nuevoId = cur.fetchall()

	idProyecto = nuevoId[0][0] # idProyecto es igual a ultimo id insertado

	sql = ("INSERT INTO `transaccion` (`transaccion`, `tipoTransaccion`, `fechahora`, `idProyecto`, `idUsuario`) VALUES ('" + transaccion + "', 'newProject', '" + str(fechahora) + "', '"+str(idProyecto)+"', '"+str(idUsuario)+"');")
	rows = get_cur(datasource).execute(sql)
	get_db(datasource).commit()


	return rows

def validCharacters(string):

	whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890$%^&*()!#@-_+/%$.,:{;[]}|?¬><~?><¿')
	string = ''.join(filter(whitelist.__contains__, string))

	return string



# A filename cannot contain any of the following characters: \ / : * ? " < > |
def validQuery(string):

	whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890$%^&()!#@-_+%$.,{;[]}')
	string = ''.join(filter(whitelist.__contains__, string))

	return string

	