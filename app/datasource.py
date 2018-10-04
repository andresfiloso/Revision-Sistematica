import MySQLdb

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
	db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="rsdb")
	return db

def get_db(self):
	return self.db

def set_cur(self):
	cur = get_db(self).cursor()
	conf=False
	return cur	

def get_cur(self):
	return self.cur




