#!/usr/bin/python
# -*- coding: utf-8 -*-

@app.route('/home',methods = ['POST', 'GET'])
def home():
	if session.get('datosUsuario') is not None:
		return redirect(url_for('projects'))
	else:
		#error = "Session Timeout"
		return render_template('login.html',)