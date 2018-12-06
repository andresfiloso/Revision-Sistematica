#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, session, url_for, request

from datasource import *
from controller import *
from models import *
from scrappingBeta import *

import jsonpickle
import os
import time

import sys
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
app.secret_key = 'super secret key'

datasource = DataSource()

@app.route('/')
def default():
    return redirect(url_for('home'),code=307)

@app.route('/home', methods = ['POST', 'GET'])
def home():
    if session.get('usuario') is not None:
        return redirect(url_for('projects'))
    else:
        #error = "Session Timeout"
        return render_template('login.html',)

@app.route('/logout', methods = ['POST', 'GET'])
def logout():
    session.clear()
    return render_template('login.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errorTemplates/pages-error-404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('errorTemplates/pages-error-500.html'), 500

@app.errorhandler(400)
def page_not_found(e):
    return render_template('errorTemplates/pages-error-400.html'), 400

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form["user"] 
        password = request.form["pass"]

        if(auth_user(user, password)):
            print "Welcome " + user
            return redirect(url_for('home'))
        else:
            session['error'] = 'Usuario o clave incorrecta!'
            return redirect(url_for('home'))


@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    return render_template('signup.html',) 

@app.route('/registrarUsuario', methods = ['POST', 'GET'])
def registrarUsuario():
    usuario = request.form["usuario"]
    email = request.form["email"]
    password = request.form["password"]
    password2 = request.form["password2"]

    if(password == password2):
        if(signup_user(usuario, email, password, password2)):
            session['status'] = "Usuario registrado correctamente"
            return redirect(url_for('home'))
        else:
            session['error'] = "Error: " + session['error_desc']
            return render_template('signup.html', **locals())
    else:
        session['error'] = "Las contraseñas no coinciden!"
        return render_template('signup.html', **locals())


@app.route('/add_user_2_project', methods = ['POST', 'GET'])
def add_user_2_project():
    usuario = request.form["usuario"]

    if(insert_colaboracion(usuario)):
        session['status'] = "Usuario invitado correctamente"
        return redirect(url_for('project'))
    else:
        session['error'] = "Error al invitar usuario"


@app.route('/micuenta',methods = ['POST', 'GET'])
def micuenta():
    if session.get('usuario') is not None:
        if session.get('proyecto') is not None:
            proyecto = get_project()
        proyectos = get_projects()
        usuario = getSession()
        
        return render_template('micuenta.html', **locals()) 
    else:
        return redirect(url_for('home'))


@app.route('/lookup',methods = ['POST', 'GET'])
def lookup():
    if session.get('usuario') is not None:
        proyectos = get_projects()
        usuario = getSession()
        if session.get('proyecto') is not None:
            proyecto = get_project()
            return render_template('lookup.html', **locals()) 
        else:
            session['error'] = "Antes de buscar articulos tienes que seleccionar un proyecto"
            return redirect(url_for('projects'))

    else:
        return redirect(url_for('home'))

@app.route('/firstProject',methods = ['POST', 'GET'])
def firstProject():
    if session.get('usuario') is not None:
        usuario = getSession()
        nombre = validCharacters(request.form["nombre"]) # issue #3 

        session['nombreProyecto'] = nombre

        return render_template('firstProject.html', **locals())
    else:
        return redirect(url_for('home'))

@app.route('/search', methods = ['POST', 'GET'])
def search():
    query = request.args.get('q', default = '*', type = str)

    return searchAPI(query)

@app.route('/scrapping',methods = ['POST', 'GET'])
def scrapping():
    session['key'] = 0
    if session.get('usuario') is not None:
        
        usuario = getSession()
        proyectos = get_projects()
        proyecto = get_project()

        keywords = request.args.get('keywords', default = '*', type = str)
        keywords2 = request.args.get('keywords2', default = '*', type = str)
        keywords3 = request.args.get('keywords3', default = '*', type = str)
        keywords4 = request.args.get('keywords4', default = '*', type = str)
        keywords5 = request.args.get('keywords5', default = '*', type = str)
        keywords6 = request.args.get('keywords6', default = '*', type = str)
        keywords7 = request.args.get('keywords7', default = '*', type = str)
        keywords8 = request.args.get('keywords8', default = '*', type = str)
        keywords9 = request.args.get('keywords9', default = '*', type = str)
        keywords10 = request.args.get('keywords10', default = '*', type = str)

        terminosKeywords = keywords.split(' AND ')
        terminosKeywords2 = keywords2.split(' AND ')
        terminosKeywords3 = keywords3.split(' AND ')
        terminosKeywords4 = keywords4.split(' AND ')
        terminosKeywords5 = keywords5.split(' AND ')
        terminosKeywords6 = keywords6.split(' AND ')

        query = ""
        print terminosKeywords


        if (keywords2 != "*"):
            for i in range(len(terminosKeywords2)):
                aux = terminosKeywords2[i]
                if(i != len(terminosKeywords2)-1):
                    query = query + keywords + " AND " + aux + " OR "
                else:
                    query = query + keywords + " AND " + aux 
        else:
            query = keywords

        print query
        
        session['keywords'] = query 

        start = time.time()

        resultados = {}

        try:
            print "INTENTANDO BUSCAR JSON"
            print "EL ARCHIVO A LLAMAR SE VA A LLAMAR: " + 'json/'+session['keywords']+'.json'
            
            with open('json/'+session['keywords']+'.json', 'r') as file:
                print "ABRI EL ARCHIVO BIEN"
                data = json.load(file)
                resultados = jsonpickle.decode(data)
                tiempoTotal = ""
                print "decodifique el archivo"
                return render_template('results.html', **locals())
            
        except:
            print "VOY A EMPEZAR A SCRAPPEAR: "
                
            data_json = searchAPI(session['keywords'])

            data_dict = json.loads(data_json)

            for key in data_dict:

                title = data_dict[key]['title']
                url = data_dict[key]['url']
                pdf = data_dict[key]['pdf']
                metadata = data_dict[key]['metadata']
                abstract = data_dict[key]['abstract']

                resultado = Resultado(key, title, url, pdf, abstract, metadata, False, False)

                resultados[key] = resultado

            end = time.time()
            tiempoTotal = end - start
            tiempoTotal = str(tiempoTotal)
            print "Tiempo de scrapping: " + str(tiempoTotal) + " segundos"

            serialized = jsonpickle.encode(resultados)

            with open('json/'+session['keywords']+'.json', 'w') as file:
                json.dump(serialized, file)

            print "Cantidad de resultados: " + str(len(resultados))  

            new_busqueda(session['keywords']);

            session['cantArticulos'] = len(resultados)

            return render_template('results.html', **locals())

    else:
        return redirect(url_for('home'))


@app.route('/article',methods = ['POST', 'GET'])
def article():
    if session.get('usuario') is not None:
        usuario = getSession()
        proyectos = get_projects()
        proyecto = get_project()

        url = request.form["url"]
        callback = request.form["callback"] # Esta variable es utilizada saber quien llamo a /article
        enProyecto = request.form["enProyecto"]

        data_json = scrap_article(url)

        data_dict = json.loads(data_json)

        title = validCharacters(data_dict['title'])
        url = data_dict['url']
        pdf = data_dict['pdf']
        abstract = validCharacters(data_dict['abstract'])
        metadata = validCharacters(data_dict['metadata'])


        # Se connstruye el objeto articulo que va a ser utilizado en el template
        articulo = Resultado(0, title, url, pdf, abstract, metadata, False, False)

        return render_template('article.html', **locals())
    else:
        return redirect(url_for('home'))

@app.route('/projects', methods = ['POST', 'GET'])
def projects():
    if session.get('usuario') is not None:
        usuario = getSession()
        proyectos = get_projects()

        if(proyectos): # at least one project
            session['noProject'] = False
            if session.get('proyecto') is not None: # Verify if there is one selected project
                proyecto = get_project()
        else: # no projects founded
            session['noProject'] = True
            session['proyecto'] = None
        return render_template('projects.html', **locals())
    else:
        return redirect(url_for('home'))

@app.route('/project', methods = ['POST', 'GET']) # All use cases tested
def project():
    if session.get('usuario') is not None:
        usuario = getSession()
        proyectos = get_projects()
        idProyecto = request.args.get('project-id')

        usuarios = get_all_users()

        print usuarios

        usuarios = json.dumps(usuarios)

        if idProyecto != None: # Call project with GET
            proyecto = get_project(idProyecto)
            busquedas = get_busquedas()
            colaboradores = get_colaboradores()
            articulos = get_articles()
            getVariablesArticles(articulos) # setea en session cantidad de clasificados, testeados, etc
            if(proyecto): # get_project returns 0 if there is no project with this id
                session['proyecto'] = proyecto.getIdProyecto()
                return render_template('project.html', **locals()) # **locals() takes all your local variables
            else:
                session['error'] = "El proyecto no existe o fue eliminado."
                return redirect(url_for('projects'))
        else: # Call project without GET
            if session.get('proyecto') is not None:
                proyecto = get_project()
                transacciones = get_transacciones()
                busquedas = get_busquedas()
                colaboradores = get_colaboradores()
                articulos = get_articles()
                getVariablesArticles(articulos) # setea en session cantidad de clasificados, testeados, etc

                return render_template('project.html', **locals()) 
            else: # session['project'] is empty
                session['error'] = "Vamos por paso. Primero, seleccciona un proyecto."
                return redirect(url_for('projects'))
    else:
        return redirect(url_for('home'))


@app.route('/newProyect',methods = ['POST', 'GET'])
def newProyect():
    if session.get('usuario') is not None:
        usuario = getSession()
        proyectos = get_projects()
        if session.get('proyecto') is not None:   
            proyecto = get_project()
        return render_template('newProyect.html', **locals())
    else:
        return redirect(url_for('home'))

@app.route('/actualizarDatos',methods = ['POST', 'GET'])
def actualizarDatos():
    if request.method == 'POST':

        usuario = request.form["usuario"]
        email = request.form["email"]

        if(update_user(usuario, email)):
            session['status'] = "Datos actualizados correctamente"
            return redirect(url_for('micuenta'))
        else:
            session['error'] = "Hubo un error al actualizar los datos"
            # Enviar aviso al admin
            return redirect(url_for('micuenta'))


@app.route('/deleteProject',methods = ['POST', 'GET'])
def deleteProject():
    if request.method == 'POST':

        idProyecto = str(request.form["idProyectoAEliminar"])

        if(delete_project(idProyecto)):
            session['status'] = "Proyecto eliminado correctamente"
            session['proyecto'] = None
            return redirect(url_for('projects'))
        else:
            session['error'] = "Hubo un error al eliminar el proyecto"
            # Enviar aviso al admin
            return redirect(url_for('projects'))


@app.route('/deleteTransaccion',methods = ['POST', 'GET'])
def deleteTransaccion():
    if request.method == 'POST':

        idTransaccion = str(request.form["idTransaccionAEliminar"])
        print "ID TRANSACCION A ELIMINAR: " + str(idTransaccion)
        if(delete_transaccion(idTransaccion)):
            session['status'] = "Transaccion eliminada correctamente"
            return redirect(url_for('project'))
        else:
            session['error'] = "Hubo un error al eliminar la transaccion"
            # Enviar aviso al admin
            return redirect(url_for('project'))


@app.route('/insertProyecto',methods = ['POST', 'GET'])
def insertProyecto():
    if request.method == 'POST':
        
        nombre = request.form["nombre"].encode('utf8')
        descripcion = request.form["descripcion"].encode('utf8')
        inclusion = request.form['inclusion'].encode('utf8')
        exclusion = request.form['exclusion'].encode('utf8')

        if(new_proyect(nombre, descripcion, inclusion, exclusion)):
            session['status'] = "Proyecto creado correctamente"
            get_projects()
            return redirect(url_for('projects'))
        else:
            session['error'] = "Error al insertar proyecto"
            # Enviar aviso al admin
            return redirect(url_for('projects'))


@app.route('/classify',methods = ['POST', 'GET'])
def classify():
    if session.get('usuario') is not None:
        usuario = getSession()
        proyectos = get_projects()
        proyecto = get_project()

        articulos = get_articles()

        print articulos

        if session.get('proyecto') is not None:
            return render_template('classify.html', **locals()) 
        else: # el proyecto no esta seleccionado
            session['error'] = "Antes de clasificar articulos tienes que seleccionar un proyecto"
            return redirect(url_for('projects'))
    else:
        return redirect(url_for('home'))


@app.route('/updateProject',methods = ['POST', 'GET'])
def updateProject():
    if request.method == 'POST':
        callback = request.args.get('callback')
        print "CALLBACK: " + callback
        idProyecto = str(request.form["idProyectoAEditar"])
        print idProyecto

        proyecto = request.form["nombre"]
        descripcion = request.form["descripcion"]
        inclusion = request.form["inclusion"]
        exclusion = request.form["exclusion"]

        if(update_project(idProyecto, proyecto, descripcion, inclusion, exclusion)):
            session['status'] = "El proyecto fue actualizado correctamente"
            return redirect(url_for(callback))
        else:
            session['error'] = "Hubo un error al actualizar el proyecto"
            # Enviar aviso al admin
            return redirect(url_for(callback))

@app.route('/updateClasificacion',methods = ['POST', 'GET'])
def updateClasificacion():
    if request.method == 'POST':
        idArticulo = str(request.form["idArticuloClasificar"])
        print idArticulo

        nuevaClasificacion = request.form["nuevaClasificacion"]
        print nuevaClasificacion

        if(update_clasificacion(idArticulo, nuevaClasificacion)):
            session['status'] = "El articulo fue actualizado correctamente"
            return redirect(url_for('classify'))
        else:
            session['error'] = "Hubo un error al actualizar el articulo"
            # Enviar aviso al admin
            return redirect(url_for('classify'))

@app.route('/addArticle',methods = ['POST', 'GET'])
def addArticle():
    if session.get('usuario') is not None:
        usuario = getSession()
        proyectos = get_projects()
        proyecto = get_project()
        tiempoTotal = ""
        idResultado = int(request.args.get('data'))
        title = request.args.get('title').encode('utf8')
        url = request.args.get('url').encode('utf8')
        test = request.args.get('test').encode('utf8')

        if(add_article(title, url, test)):
            session['status'] = "Articulo agregado correctamente"
        else:
            session['error'] = "Error al agregar articulo"

        with open('json/'+session['keywords']+'.json', 'r') as file:
                data = json.load(file)
                resultados = jsonpickle.decode(data)

        resultado = Resultado(True, True, True, True, True, True, True, True)

        for i in resultados.keys(): # recorrer con un while para bajar las interaciones
            if idResultado == resultados[i].getIdResultado():
                resultado = resultados[i]
                resultados.pop(i)

        resultado.enProyecto = True
        if(test == str(1)):
            resultado.test = True
        resultados[len(resultados) + 1] = resultado

        serialized = jsonpickle.encode(resultados)

        with open('json/'+session['keywords']+'.json', 'w') as file:
            json.dump(serialized, file)

        return "0"
    
@app.route('/deleteArticle',methods = ['POST', 'GET'])
def deleteArticle():
    if session.get('usuario') is not None:
        usuario = getSession()
        proyectos = get_projects()
        if session.get('proyecto') is not None:
            proyecto = get_project()

    tiempoTotal = ""
    resultadoAEliminar = int(request.args.get('data'))

    print "RESULTADO A ELIMINAR: "  + str(resultadoAEliminar)


    with open('json/'+session['keywords']+'.json', 'r') as file:
                data = json.load(file)
                resultados = jsonpickle.decode(data)

    for i in resultados.keys():
        if resultadoAEliminar == resultados[i].getIdResultado():
            resultados.pop(i)

    serialized = jsonpickle.encode(resultados)

    with open('json/'+session['keywords']+'.json', 'w') as file:
        json.dump(serialized, file)

    session['status'] = "Articulo borrado correctamente"

    return "0"

@app.route('/classifyArticle',methods = ['POST', 'GET'])
def classifyArticle():
    print "ESTOY EN PYTHON>>>>>"
    if session.get('usuario') is not None:
        usuario = getSession()
        proyectos = get_projects()
        if session.get('proyecto') is not None:
            proyecto = get_project()

  
    idArticulo = int(request.args.get('data'))
    clasificacion = request.args.get('clasificacion')

    print "articulo a clasificar: "  + str(idArticulo)
    print "clasificacion: "  + clasificacion

    classify_article(idArticulo, clasificacion)





    return "0"

if __name__ == "__main__":
    app.debug = True
    app.run()
    FLASK_DEBUG=1
