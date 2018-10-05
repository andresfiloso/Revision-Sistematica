from flask import session, json
from bs4 import BeautifulSoup
import requests
import re

import time

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


def scrap_article(url, pdf):
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

	keywords = html.find('div', {'class': 'keywords-section'})
	if(keywords != None):
	    keywords = keywords.text
	else:
	    keywords = "El articulo no tiene palabras claves"
 
	data = {
	    'title' : title,
	    'url' : url,
	    'abstract' : abstract,
	    'keywords' : keywords,
	    'pdf' : pdf,
	}

	end = time.time()
	tiempoTotal = end - start
	print "Tiempo de scrapping de articulo: " + str(tiempoTotal) + " segundos"

	return data

def get_scrapping_ieee():
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
		enumerationReady = '<a href="' + enumerationLink + '">' + enumeration.text + '</a>'

		metadata = ""

		for link in metadataAuthors:
			rawText = link.text
			rawlink = "https://link.springer.com" + link['href']
			linkReady = '<a href="' + rawlink + '">' + rawText + '</a>'
			metadata = metadata + linkReady + ", "


		metadata = metadata.encode('utf8') + " in " + enumerationReady.encode('utf8')
		

		print "ARTICULO: " + str(i)
		print "URL: " + url
		print "TITLE: " + title
		print "ABSTRACT: " + abstract
		print "METADATA: " + metadata

		data = {
			'id' : i,
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