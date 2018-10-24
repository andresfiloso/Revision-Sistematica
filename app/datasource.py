import sqlite3

#####################################################################
# get_db -> Devuelve un objeto conexion							 	#
#	Ejemplo: get_db(datasource).commit()						 	#	
# get_cur -> Devuelve un objeto cursos. Permite realizar queries 	#
#	Ejemplo: get_cur(datasource).execute(sql)						#
#####################################################################

class DataSource:
	def __init__(self):
		self.db = set_db()
		self.cur = set_cur(self)

def set_db():
	db = sqlite3.connect("rsdb.db", check_same_thread=False)
	db.row_factory = sqlite3.Row
	#db = sqlite3.connect(host="127.0.0.1", user="root", passwd="", db="rsdb")
	return db

def get_db(self):
	return self.db

def set_cur(self):
	cur = get_db(self).cursor()
	conf=False
	return cur	

def get_cur(self):
	return self.cur




