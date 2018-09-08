#!/usr/bin/python
# -*- coding: cp1252 -*-

import MySQLdb

# Ir al workbench y en "users and privileges" probar alguno que ande
# la mayori tienden a no andar, yo la emboque no se como
# La DB y la tabla las cree en el workbench, no se como hacerlo desde aca (todavia..)

db = MySQLdb.connect(host="127.0.0.1",    # es 127.0.1 segun el mySQL Workbench
                     user="root",         # tu usuario
                     passwd="",           # no tiene password segun Workbench
                     db="usuarios_revision") # el nombre de la base de datos

cur = db.cursor()

def crearUsuario():
    conf = False
    yaChequeado=False
    while conf == False:
        if (yaChequeado):
            print "Nombre ya ocupado. Pruebe con otro."
        user = raw_input("Ingrese usuario: ")
        passwd = raw_input("Ingrese password: ")
        if (checkUserAvailable(user)):
            conf=True
        else:
            yaChequeado=True
    
    cur.execute("INSERT INTO usuarios (Nombre,Passwd) values (%s,%s)",(user,passwd))
    db.commit()     # avisenle al forro del tutorial de mysqldb que se olvido esto, que sino no escribe la tabla.
    print "El registro fue correcto"
        


def imprimirUsuarios():
    cur.execute("SELECT nombre,passwd FROM Usuarios") #si ponemos solo name imprime los nombres de los usuarios registrados
    rows = cur.fetchall()
    for row in rows:
        for col in row:
            print "%s," % col
        print "\n"

def checkUserAvailable(nombre):
    disponible=True
    cur.execute("SELECT nombre FROM Usuarios")
    rows = cur.fetchall()
    for row in rows:
        for col in row:
            if (col == nombre):
                disponible=False
            else:
                pass
    return disponible
                

def buscarUsuario():
    exito=False
    user = raw_input("Ingrese usuario: ")
    #logdata=(user,passwd)
    cur.execute("SELECT nombre FROM Usuarios")
    rows = cur.fetchall()
    for row in rows:
        for col in row:
            if (col == user):
                exito=True
            else:
                pass
    if (exito == True):
        print "El usuario " + user + " se encuentra registrado."
    else:
        print "El usuario " + user + " NO existe en la bd."



def main():
    while True:
        print "Bienvenido al sistema: Elija opcion"
        print "1) Buscar un usuario"
        print "2) Registrarse"
        print "3) Imprimir todos los usuarios y sus contraseñas"
        opc = input("-> ")

        if (opc == 1):
            buscarUsuario()
        elif (opc == 2):
            crearUsuario()
        elif (opc == 3):
            imprimirUsuarios()
        else:
            pass

        print "Gracias por utilizar el servicio"
        print "********************************"
        print " "

main()

    

    


    
	

