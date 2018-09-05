#!/Python27/python
import cgi
form = cgi.FieldStorage()
arg = form["arg"].value
from bs4 import BeautifulSoup
import requests
import re


#springer = "https://www.springer.com/la/search?facet-type=type__cms&query=" + arg
#req = requests.get(springer)
#statusCode = req.status_code
#html = BeautifulSoup(req.text, "html.parser")
#linkSpringer = html.find_all('h4')

#elsevier = "https://www.elsevier.es/corp/?s=" + arg
#req = requests.get(elsevier)
#statusCode = req.status_code
#html = BeautifulSoup(req.text, "html.parser")
#linkElsevier = html.find_all("div", {"class": "contentText"})

urlScience = "https://www.sciencedirect.com/search?qs=" + arg + "&show=100&sortBy=relevance"
req = requests.get(urlScience)
statusCode = req.status_code
html = BeautifulSoup(req.text, "html.parser")
rawScience = html.findAll('div', {'class': 'result-item-content'})

pagination = html.find('ol', {'class': 'Pagination hor-separated-list'})




print "Content-type: text/html"
print
print "<html><head>"
print ""
print "</head><body>"
print "<p>Termino buscado: <b>%s</b></p>" %arg


print "<p>Resultados encontrados en <b>www.sciencedirect.com</b></p>"
print "Paginas: "
paginas = pagination.get_text()[10:-4]
print paginas
print "<br>"
urlPages = (int(paginas) * 100) - 100
 
print "Hay que modificar el link: "
print "https://www.sciencedirect.com/search?qs=<b>args</b>&show=100&sortBy=relevance&offset="
print urlPages


for link in rawScience:
    result = "https://www.sciencedirect.com" + link.a['href']
    print "<br>"

    req = requests.get(result)
    statusCode = req.status_code
    html = BeautifulSoup(req.text, "html.parser")
    title = html.find_all('span', {'class': 'title-text'})
    abstract = html.find_all('div', {'class': 'abstract author'})
    
    print "==========================================================================================="
    print "===========================================================================================" 

    print "<h4>"
    print title
    print "</h4>"
    print result
    print abstract

#print "<p>Resultados encontrados en <b>www.springer.com/la</b></p>"
#for link in linkSpringer:
#    ref = "https://www.springer.com" + link.a['href']
#    req = requests.get(ref)
#    statusCode = req.status_code
#    html = BeautifulSoup(req.text, "html.parser")
#    parrafos = html.find_all("p")
#
#    print "<h1>" + ref + "</h1>"
#    print "<br>"
#    print parrafos



#print "<h1>Resultados encontrados en <b>www.elsevier.es</b></h1>"
#for link in linkElsevier:
#    ref = link.a['href']
#    req = requests.get(ref)
#    statusCode = req.status_code
#    html = BeautifulSoup(req.text, "html.parser")
#    parrafos = html.find_all("p") 
#   
#    print "<h1>" + ref + "</h1>"
#    print "<br>"
#    print parrafos

print "</body></html>"
