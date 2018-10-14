from flask import session, jsonify, json
from datasource import *
from models import *
import datetime

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

	        usuario = Usuario(r[0], r[1], r[3])

	    session['usuario'] = usuario.getIdUsuario()
	    return rows

def getSession():

	cur = get_cur(datasource)

	sql = ("SELECT * FROM Usuario where idUsuario = '" + str(session['usuario']) + "'")
	rows = cur.execute(sql)

	for r in cur.fetchall():

		usuario = Usuario(r[0], r[1], r[3])

	return usuario


def get_user(idUsuario):
	cur = get_cur(datasource)

	sql = ("SELECT * FROM Usuario where idUsuario = '" + str(idUsuario) + "'")
	rows = cur.execute(sql)

	for r in cur.fetchall():

		usuario = r[1]

	return usuario

def signup_user(usuario, email, password, password2):
    sql = ("INSERT INTO `usuario` (`idUsuario`, `usuario`, `pass`, `email`) VALUES (NULL, '"+usuario+"', '"+password+"', '"+email+"');")
    rows = get_cur(datasource).execute(sql)
    get_db(datasource).commit()
    return rows

def get_projects():
	proyectos = {}
	cur = get_cur(datasource)
	sql = ("SELECT * FROM Proyecto where idUsuario = " + str(session['usuario']))
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

def get_project(*args): # sobrecarga de metodo
	if len(args) == 0: # no arguments given
		cur = get_cur(datasource)
		sql = ("SELECT * FROM Proyecto where idProyecto = " + str(session['proyecto']))
		rows = cur.execute(sql)

		#print "ROWS: " + str(rows)

		if(rows): # There should be something in rows
			for r in cur.fetchall():

				objetoProyecto = Proyecto(r[0], r[1], r[2], r[3], r[4])

		else: # Return 0, there is no project with this id
			return rows

		#print session['transacciones']
		return objetoProyecto
	if len(args) == 1:
		cur = get_cur(datasource)
		sql = ("SELECT * FROM Proyecto where idProyecto = " + args[0])
		rows = cur.execute(sql)

		if(rows): # There should be something in rows
			for r in cur.fetchall():

				objetoProyecto = Proyecto(r[0], r[1], r[2], r[3], r[4])

			session['proyecto'] = objetoProyecto.getIdProyecto()
		else: # Return 0, there is no project with this id
			return rows

		return objetoProyecto

	if len(args) == 2:
		if(args[1] == False): # Bussiness rule. No seleccionar proyecto
			cur = get_cur(datasource)
			sql = ("SELECT * FROM Proyecto where idProyecto = " + args[0])
			rows = cur.execute(sql)

			for r in cur.fetchall():

				objetoProyecto = Proyecto(r[0], r[1], r[2], r[3], r[4])

			return objetoProyecto




def get_transacciones():
	cur = get_cur(datasource)
	sql = ("SELECT * FROM Transaccion where idProyecto = " + str(session['proyecto']))
	rows = cur.execute(sql)

	transacciones = {}

	i = 0
	for r in cur.fetchall():

		transaccion = Transaccion(r[0], r[1], r[2], r[3], get_project().getProyecto(), get_user(r[5]))

		transacciones[i] = transaccion
		i +=1

	return transacciones


def get_busquedas():
	cur = get_cur(datasource)
	sql = ("SELECT * FROM Busqueda where idProyecto = " + str(session['proyecto']))
	rows = cur.execute(sql)

	busquedas = {}

	i = 0
	for r in cur.fetchall():

		busqueda = Busqueda(r[0], r[1], r[2], get_project().getProyecto(), get_user(r[4]))

		busquedas[i] = busqueda
		i +=1

	return busquedas

def new_busqueda(query):
	usuario = getSession()

	now = datetime.datetime.now()
	fechahora = now.strftime("%Y-%m-%d %H:%M")

	sql = ("INSERT INTO `busqueda` (`busqueda`, `fechahora`, `idProyecto`, `idUsuario`) VALUES ('" + query + "', '" + str(fechahora) + "', '"+str(session['proyecto'])+"', '"+str(usuario.getIdUsuario())+"');")
	rows = get_cur(datasource).execute(sql)
	get_db(datasource).commit()

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

def update_project(idProyecto, proyecto, descripcion, inclusion, exclusion):

	proyectoAnterior =  get_project(idProyecto, False)

	idUsuario = str(session['usuario'])
	sql = ("UPDATE `proyecto` SET `proyecto` = '" + proyecto + "', `descripcion` = '" + descripcion + "', `inclusion` = '" + inclusion + "', `exclusion` = '" + exclusion + "' WHERE `proyecto`.`idProyecto` = '" + idProyecto + "';")
	rows = get_cur(datasource).execute(sql)
	get_db(datasource).commit()

	usuario = getSession()

	transaccion = usuario.getUsuario() + " edito el proyecto " + proyectoAnterior.getProyecto()
	now = datetime.datetime.now()
	fechahora = now.strftime("%Y-%m-%d %H:%M")

	sql = ("INSERT INTO `transaccion` (`transaccion`, `tipoTransaccion`, `fechahora`, `idProyecto`, `idUsuario`) VALUES ('" + transaccion + "', 'updateProject', '" + str(fechahora) + "', '"+str(idProyecto)+"', '"+str(usuario.getIdUsuario())+"');")
	rows = get_cur(datasource).execute(sql)
	get_db(datasource).commit()

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

	