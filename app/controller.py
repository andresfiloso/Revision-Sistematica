from flask import session, jsonify, json
from datasource import *
from models import *
import datetime
import pickle

datasource = DataSource()

#####################################################################
# DataSource es un objteo que permite el acceso a la base de datos.	#
# Informacion de esta clase en datasource.py 						#
#####################################################################

def auth_user(user, password):
	cur = get_cur(datasource)

	sql = ("SELECT * FROM Usuario where usuario = '" + user + "' and pass = '" + password + "'")
	rows = cur.execute(sql)

	if rows == 1: #Autenticacion correcta

	    for r in cur.fetchall():

	        datosUsuario = {
	            'idUsuario' : r[0],
	            'usuario' : r[1],
	            'email' : r[3]
	        }

	    session['datosUsuario'] = datosUsuario
	    session['pickle'] = pickle
	    return rows



def signup_user(usuario, email, password, password2):
    sql = ("INSERT INTO `usuario` (`idUsuario`, `usuario`, `pass`, `email`) VALUES (NULL, '"+usuario+"', '"+password+"', '"+email+"');")
    rows = get_cur(datasource).execute(sql)
    get_db(datasource).commit()
    return rows

def get_projects():
	proyectos = {}
	cur = get_cur(datasource)
	sql = ("SELECT * FROM Proyecto where idUsuario = " + str(session['datosUsuario']['idUsuario']))
	rows = cur.execute(sql)

	print "ROWS: " + str(rows)
	if (rows): # At least, there is one project
		i = 0

		for r in cur.fetchall():

			objetoProyecto = Proyecto(r[0], r[1], r[2], r[3], r[4])
			print objetoProyecto
			proyectos[i] = objetoProyecto
			i += 1
	else:
		return rows

	return proyectos

def get_project(idProyecto):
	cur = get_cur(datasource)
	sql = ("SELECT * FROM Proyecto where idProyecto = " + idProyecto)
	rows = cur.execute(sql)

	#print "ROWS: " + str(rows)

	if(rows): # There should be something in rows
		for r in cur.fetchall():

			objetoProyecto = Proyecto(r[0], r[1], r[2], r[3], r[4])

		#print objetoProyecto

		#print objetoProyecto.getIdProyecto()	

	else: # Return 0, there is no project with this id
		return rows

	sql = ("SELECT * FROM Transaccion where idProyecto = " + idProyecto)
	rows = cur.execute(sql)

	transacciones = {}

	i = 0
	for r in cur.fetchall():

		transaccion = {
		    'idTransaccion': r[0],
		    'transaccion': r[1],
		    'tipoTransaccion': r[2],
		    'fechahora': r[3],
		    'idProyecto': r[4],
		    'idUsuario': r[5]
		}

		transacciones[i] = transaccion
		i +=1

	session['transacciones'] = transacciones

	#print session['transacciones']
	return objetoProyecto

def update_user(usuario, email):
	idUsuario = str(session['datosUsuario']['idUsuario'])
	sql = ("UPDATE `usuario` SET `usuario` = '" + usuario + "', `email` = '" + email + "' WHERE `usuario`.`idUsuario` = '" + idUsuario + "';")
	rows = get_cur(datasource).execute(sql)
	get_db(datasource).commit()

	datosUsuario = {
		'idUsuario' : idUsuario,
		'usuario' : usuario,
		'email' : email
	}
	session['datosUsuario'] = datosUsuario
	return rows

def update_project(idProyecto, proyecto, descripcion, inclusion, exclusion):
	idUsuario = str(session['datosUsuario']['idUsuario'])
	sql = ("UPDATE `proyecto` SET `proyecto` = '" + proyecto + "', `descripcion` = '" + descripcion + "', `inclusion` = '" + inclusion + "', `exclusion` = '" + exclusion + "' WHERE `proyecto`.`idProyecto` = '" + idProyecto + "';")
	rows = get_cur(datasource).execute(sql)
	get_db(datasource).commit()
	return rows

def delete_project(idProyecto):
	idUsuario = str(session['datosUsuario']['idUsuario'])
	sql = ("DELETE FROM `proyecto` WHERE `proyecto`.`idProyecto` = '" + idProyecto + "';")
	rows = get_cur(datasource).execute(sql)
	get_db(datasource).commit()
	return rows

def new_proyect(nombre, descripcion, inclusion, exclusion):
	idUsuario = str(session['datosUsuario']['idUsuario'])
	sql = ("INSERT INTO `Proyecto` (`proyecto`, `descripcion`, `inclusion`, `exclusion`, `idUsuario`) VALUES ('" + nombre + "', '" + descripcion + "', '" + inclusion + "', '" + exclusion + "', '" + idUsuario + "')")
	rows = get_cur(datasource).execute(sql)
	get_db(datasource).commit()

	transaccion = session['datosUsuario']['usuario'] + " creo el proyecto " + nombre
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

	