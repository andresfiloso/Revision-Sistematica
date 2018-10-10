from flask import session
from datasource import *
from models import *



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

	i = 0
	for r in cur.fetchall():

		proyecto = {
		'idProyecto' : r[0],
		'proyecto' : r[1],
		'descripcion' : r[2],
		'inclusion': r[3],
		'exclusion': r[4]
		}

		proyectos[i] = proyecto
		i += 1
	session['proyectos'] = proyectos

	return rows

def get_project(idProyecto):
	cur = get_cur(datasource)
	sql = ("SELECT * FROM Proyecto where idProyecto = " + idProyecto)
	rows = cur.execute(sql)

	for r in cur.fetchall():

		proyecto = {
		    'idProyecto': r[0],
		    'proyecto': r[1],
		    'descripcion': r[2],
		    'inclusion': r[3],
		    'exclusion': r[4]
		}

		session['proyecto'] = proyecto
	return rows

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
	return rows

	