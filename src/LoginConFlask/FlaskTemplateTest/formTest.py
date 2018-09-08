from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def student():
    return render_template('student.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form       #usar request.form porque request.get_json() no funciona
        print "Valores: "
        for key,value in result.iteritems():        #result contiene un diccionario con los valores
            print  key +" "+ value #Imprime el campo y value, que  es lo que tenemos que extraer!!

    return  render_template("result.html",result = result) #para que despues lo mande al otro .html

if __name__ == '__main__':
    app.run()

