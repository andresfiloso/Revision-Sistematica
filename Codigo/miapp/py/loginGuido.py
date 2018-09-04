#!/usr/bin/python

import MySQLdb

# Ir al workbench y en "users and privileges" probar alguno que ande
# la mayori tienden a no andar, yo la emboque no se como
# La DB y la tabla las cree en el workbench, no se como hacerlo desde aca (todavia..)

db = MySQLdb.connect(host="127.0.0.1",    # es 127.0.1 segun el mySQL Workbench
                     user="root",         # tu usuario
                     passwd="",           # no tiene password segun Workbench
                     db="usuarios_revision") # el nombre de la base de datos



cur = db.cursor()
conf=False

def crearUsuario():
    user = raw_input("Ingrese usuario: ")
    passwd = raw_input("Ingrese password: ")
    cur.execute("INSERT INTO usuarios (Nombre,Passwd) values (%s,%s)",(user,passwd))
    conf=True
    db.commit()     # avisenle al forro del tutorial de mysqldb que se olvido esto, que sino no escribe la tabla.
    print "El registro fue correcto"
    db.close()
    cur.close()

def imprimirUsuarios():
    cur.execute("SELECT nombre,passwd FROM Usuarios")
    rows = cur.fetchall()
    for row in rows:
        for col in row:
            print "%s," % col
        print "\n"