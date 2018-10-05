#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, session, url_for, request

from datasource import *
from controller import *
from models import *
from scrapping import *

import os
import time

app = Flask(__name__)
app.secret_key = 'super secret key'

datasource = DataSource()

@app.route('/')
def default():
    return redirect(url_for('home'),code=307)

@app.route('/home', methods = ['POST', 'GET'])
def home():
    if session.get('datosUsuario') is not None:
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

    if(signup_user(usuario, email, password, password2)):
        session['status'] = "Usuario registrado correctamente"
        return redirect(url_for('home'))
    else:
        session['error'] = "Error al registrar usuario"


@app.route('/lookup',methods = ['POST', 'GET'])
def lookup():
    if session.get('datosUsuario') is not None:
        if session.get('proyecto') is not None:

            return render_template('lookup.html') 
        else:
            session['error'] = "Antes de buscar articulos tienes que seleccionar un proyecto"
            return redirect(url_for('projects'))

    else:
        return redirect(url_for('home'))


@app.route('/micuenta',methods = ['POST', 'GET'])
def micuenta():
    if session.get('datosUsuario') is not None:
        return render_template('micuenta.html',) 
    else:
        return redirect(url_for('home'))

@app.route('/results',methods = ['POST', 'GET'])
def results():
    if session.get('datosUsuario') is not None:
        if session.get('proyecto') is not None:
            keywords = request.args.get('keywords', default = '*', type = str)
            newKeyword = request.args.get('newKeyword', default = '*', type = str)

            session['keywords'] = keywords

            return render_template('results.html', keywords = keywords)
        else:
            session['error'] = "Antes de buscar articulos tienes que seleccionar un proyecto"
            return redirect(url_for('projects'))
    else: 
        return redirect(url_for('home'))


@app.route('/scrapping',methods = ['POST', 'GET'])
def scrapping():

    return get_scrapping_springer()

@app.route('/article',methods = ['POST', 'GET'])
def article():
    if session.get('datosUsuario') is not None:
        print "ingreso a requestear el formulario"
        url = request.form["url"]
        print url
        page = request.form["page"]
        print page
        pdf = request.form["pdf"]
        print pdf

        #abstract =  rawAbstract.replace('Abstract', '<h2 class="card-title">Abstract</h2>')
        print "Se va a ir a scrap_article"
        session['article'] = scrap_article(url, page, pdf)

        return render_template('article.html')
    else:
        return redirect(url_for('home'))
    


@app.route('/projects',methods = ['POST', 'GET'])
def projects():
    if session.get('datosUsuario') is not None:

        get_projects()

        return render_template('projects.html')
    else:
        return redirect(url_for('home'))


@app.route('/newProyect',methods = ['POST', 'GET'])
def newProyect():
    if session.get('datosUsuario') is not None:
        return render_template('newProyect.html')
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
            return redirect(url_for('projects'))
        else:
            session['error'] = "Hubo un error al eliminar el proyecto"
            # Enviar aviso al admin
            return redirect(url_for('projects'))



@app.route('/insertProyecto',methods = ['POST', 'GET'])
def insertProyecto():
    if request.method == 'POST':
        
        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]
        inclusion = request.form['inclusion']
        exclusion = request.form['exclusion']

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
    if session.get('datosUsuario') is not None:
        idProyecto = request.args.get('project-id')
        print "IDPROYECTO: " + str(idProyecto)

        if idProyecto != None: # se llama a classify con get
            if(get_project(idProyecto)):
                return render_template('classify.html')
            else: # no se encontro el idProyecto en la bd
                session['error'] = "El proyecto no existe o fue eliminado"
                return redirect(url_for('projects'))
        else: # se llama a classify sin get
            if session.get('proyecto') is not None:
                return render_template('classify.html') 
            else: # el proyecto no esta seleccionado
                session['error'] = "Antes de clasificar articulos tienes que seleccionar un proyecto"
                return redirect(url_for('projects'))
    else:
        return redirect(url_for('home'))


@app.route('/updateProject',methods = ['POST', 'GET'])
def updateProject():
    if request.method == 'POST':
        idProyecto = str(request.form["idProyectoAEditar"])
        print idProyecto

        proyecto = request.form["nombre"]
        descripcion = request.form["descripcion"]
        inclusion = request.form["inclusion"]
        exclusion = request.form["exclusion"]

        if(update_project(idProyecto, proyecto, descripcion, inclusion, exclusion)):
            session['status'] = "El proyecto fue actualizado correctamente"
            return redirect(url_for('projects'))
        else:
            session['error'] = "Hubo un error al actualizar el proyecto"
            # Enviar aviso al admin
            return redirect(url_for('projects'))


if __name__ == "__main__":
    app.debug = True
    app.run()
