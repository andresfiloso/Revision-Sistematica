from flask import session, json
from bs4 import BeautifulSoup
import requests
import re

import time


########################################################################
# Switcher: selecciona el articulo y lo parsea dependiendo de la fuente
########################################################################

def scrap_article(url, page,  pdf):
	if(page == "ScienceDirect"):
		return scrap_article_sciencedirect(url, page, pdf)
	if(page == "Springer"):
		return scrap_article_springer(url, page, pdf)
	if(page == "IEEE Xplore"):
		return scrap_article_ieee(url, page, pdf)

########################################################################
########################################################################

def get_scrapping_full():
	start = time.time()
	urlScience = "https://www.sciencedirect.com/search?qs=" + session['keywords'] + "&show=10&sortBy=relevance"
	print urlScience
	req = requests.get(urlScience)
	statusCode = req.status_code
	html = BeautifulSoup(req.text, "html.parser")
	rawScience = html.findAll('div', {'class': 'result-item-content'})

	data_ready = {}

	dataArray = {}

	i = 0

	for link in rawScience:
		if(i < 5):
			result = "https://www.sciencedirect.com" + link.a['href']
			print result
			req = requests.get(result)
			statusCode = req.status_code
			html = BeautifulSoup(req.text, "html.parser")
			title = html.find('span', {'class': 'title-text'})
			if(title != None):
			    title = title.text
			else:
			    title = "El articulo no tiene titulo"
			abstract = html.find('div', {'class': 'abstract author'})
			if(abstract != None):
			    abstract = abstract.text
			else:
			    abstract = "El articulo no tiene abstract"
			keywords = html.find('div', {'class': 'keywords-section'})
			if(keywords != None):
			    keywords = keywords.text
			else:
			    keywords = "El articulo no tiene palabras claves"

			data = {
			    'id' : i,
			    'title' : title,
			    'result' : result,
			    'abstract' : abstract,
			    'keywords' : keywords
			}

			print title.encode('utf8')
			print result.encode('utf8')
			print abstract.encode('utf8')
			print keywords.encode('utf8')

			dataArray[i] = data

			i = i+1

	print "Cantidad de articulos: " + str(i)

	session['cantArticulos'] = i
	data_ready = json.dumps(dataArray)

	end = time.time()
	tiempoTotal = end - start
	print "Tiempo de scrapping: " + str(tiempoTotal) + " segundos"
	print "Tiempo por articulo: " + str(tiempoTotal / i) + " segundos"

	return data_ready

######################################################################################################################################
########################################################## SCIENCE DIRECT ############################################################
######################################################################################################################################

def get_scrapping_url():
	start = time.time()
	urlScience = "https://www.sciencedirect.com/search?qs=" + session['keywords'] + "&show=100&sortBy=relevance&offset=0"
	print urlScience
	req = requests.get(urlScience)
	statusCode = req.status_code
	html = BeautifulSoup(req.text, "html.parser")
	rawScience = html.findAll('div', {'class': 'result-item-content'})

	data_ready = {}

	dataArray = {}

	i = 0

	for div in rawScience:
	
		url = "https://www.sciencedirect.com" + div.a['href']
		print "ARTICULO: " + str(i)
		title = div.a.text
		print "TITLE: " + title.encode('utf8')
		print "URL: " + url


		info = div.find('div', {'id': lambda L: L and L.startswith('aa-srp-result-list-srctitle')})
		authors = div.find('ol', {'class': 'Authors'})
		pdf = div.find('li', {'class': 'DownloadPdf'})

		if(info != None):
			info = info.text
		else:
			info = "El info no tiene info"

		if(authors != None):
			authors = authors.text
		else:
			authors = "No hay autores"

		if(pdf != None):
			pdf = "https://www.sciencedirect.com" + pdf.a['href']
		else:
			pdf = str(0)

		print "PDF: " + str(pdf)

		data = {
		    'id' : i,
		    'page' : "ScienceDirect",
		    'title' : title,
		    'result' : url,
		    'info' : info,
		    'authors' : authors,
		    'pdf' : pdf,
		}

		dataArray[i] = data

		i = i+1

	print "Cantidad de articulos: " + str(i)

	session['cantArticulos'] = i
	data_ready = json.dumps(dataArray)

	end = time.time()
	tiempoTotal = end - start
	session['lookup_time'] = str(tiempoTotal) + " segundos"
	print "Tiempo de scrapping: " + str(tiempoTotal) + " segundos"
	print "Tiempo por articulo: " + str(tiempoTotal / i) + " segundos"

	return data_ready

def scrap_article_sciencedirect(url, page, pdf):
	start = time.time()

	req = requests.get(url)
	statusCode = req.status_code
	html = BeautifulSoup(req.text, "html.parser")

	title = html.find('span', {'class': 'title-text'})
	if(title != None):
		title = title.text
	else:
		title = "El articulo no tiene titulo"

	abstract = html.find('div', {'class': 'abstract author'})
	if(abstract != None):
	    abstract = abstract.text
	else:
	    abstract = "El articulo no tiene abstract"

	keywordsRaw = html.findAll('div', {'class': 'keyword'})

	keywords = ""
	for keyword in keywordsRaw:
		keySpan = keyword.find('span').text
		keywords = keywords + ", " + str(keySpan)


	if(keywords != None):
	    keywords = "KeyWords: " + keywords 
	else:
	    keywords = "El articulo no tiene palabras claves"
 
	data = {
		'title' : title,
		'page' : page,
		'url' : url,
		'abstract' : abstract,
		'keywords' : keywords,
		'pdf' : pdf,
	}

	end = time.time()
	tiempoTotal = end - start
	print "Tiempo de scrapping de articulo: " + str(tiempoTotal) + " segundos"

	return data

######################################################################################################################################
########################################################## SPRINGER ##################################################################
######################################################################################################################################

def get_scrapping_springer():
	start = time.time()
	url = 'https://link.springer.com/search?&query=' + session['keywords'] + '&facet-content-type="ConferencePaper"&showAll=true'
	print url
	req = requests.get(url)
	statusCode = req.status_code
	html = BeautifulSoup(req.text, "html.parser")
	ol = html.find('ol', {'class': 'content-item-list'})
	li = ol.findAll('li')


	data_ready = {}

	dataArray = {}

	i = 0



	for result in li:
		link = result.find('a', {'class': 'title'})
		url = "https://link.springer.com" + link['href']
		title = link.text.encode('utf8')
		abstract = result.find('p', {'class': 'snippet'}).text.encode('utf8').strip()
		metaRaw = result.find('p', {'class': 'meta'})

		authors = metaRaw.find('span', {'class': 'authors'})
		enumeration = metaRaw.find('span', {'class': 'enumeration'})
		metadataAuthors = authors.findAll('a')

		enumerationLink = "https://link.springer.com" + enumeration.find('a')['href']
		enumerationReady = '<a href="' + enumerationLink + '" target="_blank">' + enumeration.text + '</a>'

		metadata = ""

		for link in metadataAuthors:
			rawText = link.text
			rawlink = "https://link.springer.com" + link['href']
			linkReady = '<a href="' + rawlink + '" target="_blank">' + rawText + '</a>'
			metadata = metadata + linkReady + ", "


		metadata = metadata.encode('utf8') + " in " + enumerationReady.encode('utf8')
		

		print "ARTICULO: " + str(i)
		print "URL: " + url
		print "TITLE: " + title
		print "ABSTRACT: " + abstract
		print "METADATA: " + metadata

		data = {
			'id' : i,
			'page' : "Springer",
			'title' : title,
			'result' : url,
			'abstract' : abstract,
			'metadata' : metadata,
		}
		
		dataArray[i] = data

		i = i+1

	print "Cantidad de articulos: " + str(i)

	session['cantArticulos'] = i
	data_ready = json.dumps(dataArray)

	end = time.time()
	tiempoTotal = end - start
	session['lookup_time'] = str(tiempoTotal) + " segundos"
	print "Tiempo de scrapping: " + str(tiempoTotal) + " segundos"
	print "Tiempo por articulo: " + str(tiempoTotal / i) + " segundos"

	return data_ready

def scrap_article_springer(url, page, pdf):
	start = time.time()

	req = requests.get(url)
	statusCode = req.status_code
	html = BeautifulSoup(req.text, "html.parser")

	title = html.find('h1', {'class': 'ChapterTitle'})
	if(title != None):
		title = title.text
	else:
		title = "El articulo no tiene titulo"

	abstract = html.find('p', {'class': 'Para'})
	if(abstract != None):
	    abstract = 'Abstract' + abstract.text
	else:
	    abstract = "El articulo no tiene abstract"

	keywords = html.find('div', {'class': 'keywords-section'})
	if(keywords != None):
	    keywords = keywords.text
	else:
	    keywords = "Springer no tiene palabras claves"
 
	data = {
	    'title' : title,
		'page' : page,
	    'url' : url,
	    'abstract' : abstract,
	    'keywords' : keywords,
	    'pdf' : '0',
	}

	end = time.time()
	tiempoTotal = end - start
	print "Tiempo de scrapping de articulo: " + str(tiempoTotal) + " segundos"

	return data


######################################################################################################################################
########################################################## IEEE Xplore ###############################################################
######################################################################################################################################

def get_scrapping_ieee():
	start = time.time()
	url = 'https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText=' + session['keywords']
	print url
	req = requests.get(url)
	statusCode = req.status_code
	html = BeautifulSoup(req.text, "html.parser")
	divMain = html.find('div', {'class': 'main-section'})
	results = divMain.findAll('div', {'class': 'List-results-items'})


	data_ready = {}

	dataArray = {}

	i = 0

	for result in results:
		link = result.find('h2')
		print link.text.encode('utf8')
		
	end = time.time()
	tiempoTotal = end - start
	session['lookup_time'] = str(tiempoTotal) + " segundos"
	print "Tiempo de scrapping: " + str(tiempoTotal) + " segundos"
	print "Tiempo por articulo: " + str(tiempoTotal / i) + " segundos"

	return data_ready