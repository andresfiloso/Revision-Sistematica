# -*- coding: utf-8 -*-
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

			dataArray[i] = data

			i = i+1

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

def get_scrapping_sciencedirect():
	start = time.time()
	urlScience = "https://www.sciencedirect.com/search?qs=" + session['keywords'] + "&show=100&sortBy=relevance&offset=0"
	req = requests.get(urlScience)
	statusCode = req.status_code
	html = BeautifulSoup(req.text, "html.parser")
	rawScience = html.findAll('div', {'class': 'result-item-content'})

	data_ready = {}

	dataArray = {}

	i = 0

	for div in rawScience:
	
		url = "https://www.sciencedirect.com" + div.a['href']
		title = div.a.text
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

		data = {
		    'id' : "sd" + str(i),
		    'page' : "ScienceDirect",
		    'title' : title,
		    'result' : url,
		    'info' : info,
		    'authors' : authors,
		    'pdf' : pdf,
		}

		dataArray[session['key']] = data
		i += 1
		session['key'] += 1

	session['cantArticulos'] = i

	end = time.time()
	tiempoTotal = end - start
	session['lookup_time'] = str(tiempoTotal) + " segundos"
	print "Tiempo de scrapping: " + str(tiempoTotal) + " segundos"
	print "Tiempo por articulo: " + str(tiempoTotal / i) + " segundos"

	print "DATA READY TYPE: SCIENCE DIRECT " + str(type(data_ready))

	return dataArray

	############################################
	######## ARTICLE SCIENCE DIRECT ############
	############################################

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
		keywords = keywords + ", " + keySpan


	if(keywords != None):
	    keywords = "KeyWords: " + keywords
	else:
	    keywords = "El articulo no tiene palabras claves"

	print keywords
 
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

		enumerationLink = "https://link.springer.com" + enumeration.find('a')['href']
		enumerationReady = '<a href="' + enumerationLink + '" target="_blank">' + enumeration.text + '</a>'
		
		if authors is not None:
			metadataAuthors = authors.findAll('a')
			metadata = ""
			for link in metadataAuthors:
				rawText = link.text
				rawlink = "https://link.springer.com" + link['href']
				linkReady = '<a href="' + rawlink + '" target="_blank">' + rawText + '</a>'
				metadata = metadata + linkReady + ", "
			metadata = metadata[:-2] #quito la ultima coma de los autores
			metadata = metadata.encode('utf8') + " in " + enumerationReady.encode('utf8')
		else:
			metadata = enumerationReady.encode('utf8')

		data = {
			'id' : "sp" + str(i),
			'page' : "Springer",
			'title' : title,
			'result' : url,
			'abstract' : abstract,
			'metadata' : metadata,
		}
		
		dataArray[session['key']] = data

		i += 1
		session['key'] += 1

	session['cantArticulos'] = i

	end = time.time()
	tiempoTotal = end - start
	session['lookup_time'] = str(tiempoTotal) + " segundos"
	print "Tiempo de scrapping: " + str(tiempoTotal) + " segundos"
	print "Tiempo por articulo: " + str(tiempoTotal / i) + " segundos"

	print "DATA READY TYPE: SPRINGER " + str(type(data_ready))

	return dataArray

	############################################
	######## ARTICLE SPRINGER ##################
	############################################

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
	keywords = session['keywords']

	search_request = {
                'newsearch': True,
                'queryText': keywords,

    }

	headers = {
				'User-Agent':'BeautifulSoup, contact me at andresfilosok@gmail.com', 
				'Referer':'https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText=' + keywords, 
				'Content-type': 'application/json'
	}

	payload = json.dumps(search_request)
	req = requests.post('https://ieeexplore.ieee.org/rest/search', data=payload ,headers=headers)	
	statusCode = req.status_code
	json_data = req.text
	item_dict = json.loads(json_data)

	data_ready = {}

	dataArray = {}

	cantidadArticulos = len(item_dict['records'])
	for i in range(cantidadArticulos):
		try:  url = "https://ieeexplore.ieee.org" + item_dict['records'][i]['documentLink']
		except: url = "No url"
		print "URL: " + url

		try: title = item_dict['records'][i]['articleTitle']
		except: title = "No title"
		
		try: articleNumber = item_dict['records'][i]['articleNumber']
		except: articleNumber = "No articleNumber"

		try: publicationTitle = item_dict['records'][i]['publicationTitle']
		except: publicationTitle = "No publicationTitle"

		try: publicationLink = "https://ieeexplore.ieee.org" + item_dict['records'][i]['publicationLink']
		except: publicationLink = "No publicationLink"

		try: abstract = item_dict['records'][i]['abstract']
		except: abstract = "No abstract"

		try: 
			cantidadAutores = len(item_dict['records'][i]['authors'])
			print "Cantidad de autores: " + str(cantidadAutores)
			for j in range(cantidadAutores):
				authors = item_dict['records'][i]['authors'][j]['preferredName']
				if j == 0:	
					metadata = authors
				else:
					metadata = metadata + ", " + authors
		except: 
			cantidadAutores = "No authors"		

		data = {
			'id' : "ie" + str(i),
			'page' : "IEEE Xplore",
			'title' : title,
			'result' : url,
			'articleNumber' : articleNumber,
			'abstract' : abstract,
			'metadata' : metadata,
		}
		
		dataArray[session['key']] = data
		session['key'] +=1

	session['cantArticulos'] = cantidadArticulos
		
	end = time.time()
	tiempoTotal = end - start
	session['lookup_time'] = str(tiempoTotal) + " segundos"
	print "Tiempo de scrapping: " + str(tiempoTotal) + " segundos"
	print "Tiempo por articulo: " + str(tiempoTotal / cantidadArticulos) + " segundos"

	print "DATA READY TYPE IEEE: " + str(type(data_ready))

	return dataArray

	############################################
	############ ARTICLE IEEE ##################
	############################################

def scrap_article_ieee(articleNumber, page, pdf):
	start = time.time()

	headers = {
				'User-Agent':'BeautifulSoup, contact me at andresfilosok@gmail.com', 
				'Referer': 'https://ieeexplore.ieee.org/document/' + articleNumber,
				'Content-type': 'application/json'
	}

	urlSnippet = "https://ieeexplore.ieee.org/rest/document/" + articleNumber + "/snippet"
	req = requests.get(urlSnippet, headers=headers)
	statusCode = req.status_code
	html = BeautifulSoup(req.text, "html.parser")

	introduction = html.find('h3')
	snippet = html.find('p')

	if (introduction != None):
		introduction = introduction.text
	else:
		introduction = ""

	if (snippet != None):
		snippet = snippet.text
	else:
		snippet = "No se encontro informacion para mostrar"

	snippet = introduction + snippet

	urlSimilar = "https://ieeexplore.ieee.org/rest/document/" + articleNumber + "/similar"
	req = requests.get(urlSimilar, headers=headers)
	json_data = req.text
	item_dict = json.loads(json_data)

	title = item_dict['title']

	url = "https://ieeexplore.ieee.org/document/" + articleNumber
 	
	data = {
	    'title' : title,
		'page' : page,
	    'url' : url,
	    'abstract' : snippet,
	    'keywords' : "No hay palabras claves",
	    'pdf' : '0',
	}

	end = time.time()
	tiempoTotal = end - start
	print "Tiempo de scrapping de articulo: " + str(tiempoTotal) + " segundos"
	


	return data
