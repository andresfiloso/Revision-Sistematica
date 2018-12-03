# -*- coding: utf-8 -*-
from flask import session, json
from bs4 import BeautifulSoup
import requests
import re
import io
from models import *
from datetime import datetime

import time

import sys
reload(sys)
sys.setdefaultencoding('utf8')


def scrap_article(url):

	if "www.sciencedirect.com" in url:return scienceDirect_articleAPI(url)
	elif "link.springer.com" in url: return springer_articleAPI(url)
	elif "ieeexplore.ieee.org" in url: return ieeeXplore_articleAPI(url)

######################################################################################################################################
########################################################## SCIENCE DIRECT ############################################################
######################################################################################################################################

def scienceDirectAPI(query):
	url = 'https://api.elsevier.com/content/search/sciencedirect?start=25&count=25&query='+ query +'&apiKey=7f59af901d2d86f78a1fd60c1bf9426a'
	headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
	r = requests.get(url, headers=headers).json()
	results = json.dumps(r)

	#print results

	data = json.loads(results)

	response = {}

	try:
		almost_one = data["search-results"]["entry"]

		for i in range(25):
		
			print "entry -> " + str(i)

			title = data["search-results"]["entry"][i]["dc:title"].encode("utf-8")
			print title
			url = "https://www.sciencedirect.com/science/article/pii/" + data["search-results"]["entry"][i]["pii"].encode("utf-8")
			openaccess = data["search-results"]["entry"][i]["openaccess"]
			if data["search-results"]["entry"][i]["authors"] is not None:
				author = data["search-results"]["entry"][i]["dc:creator"].encode("utf-8")
			else:
				author = "No Author"
			date = data["search-results"]["entry"][i]["prism:coverDate"].encode("utf-8")
			publicationName = data["search-results"]["entry"][i]["prism:publicationName"].encode("utf-8")
			metadata = author + " - " + publicationName + ", " + date

			response[i] = {
					"title" : title,
					"url": url,
					"pdf": openaccess,
					"abstract": "No abstract available",
					"metadata": metadata,
					}


		data = json.dumps(response, indent=4, sort_keys=True)

	except:
		data = json.dumps(response, indent=4, sort_keys=True)
		return data

	#print data

	return data


######################################################################################################################################
########################################################## IEEE Xplore ###############################################################
######################################################################################################################################

def ieeeXploreAPI(query):

	search_request = {
                'newsearch': True,
                'queryText': query,
    }

	headers = {
				'User-Agent':'BeautifulSoup, contact me at andresfilosok@gmail.com', 
				'Referer':'https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText=' + query, 
				'Content-type': 'application/json'
	}

	payload = json.dumps(search_request)
	r = requests.post('https://ieeexplore.ieee.org/rest/search', data=payload, headers=headers).json()
	results = json.dumps(r)

	print results

	data = json.loads(results)
	response = {}

	authors = ""

	if data['endRecord'] != 0:

		cantidadArticulos = len(data['records'])

		for i in range(cantidadArticulos):

			try: abstract = data['records'][i]['abstract'].encode("utf-8")
			except: abstract = "No abstract"

			try: title = data['records'][i]['articleTitle'].encode("utf-8")
			except: title = "No title"

			try:  url = "https://ieeexplore.ieee.org" + data['records'][i]['documentLink'].encode("utf-8")
			except: url = "No url"
			#print "URL: " + url

			try: publicationTitle = data['records'][i]['publicationTitle'].encode("utf-8")
			except: publicationTitle = "No publicationTitle"

			try: publicationYear = data['records'][i]['publicationYear'].encode("utf-8")
			except: publicationYear = "No publication Year"


			try: 
				cantidadAutores = len(data['records'][i]['authors'])
				#print "Cantidad de autores: " + str(cantidadAutores)
				for j in range(cantidadAutores):
					authorsRaw = data['records'][i]['authors'][j]['normalizedName'].encode("utf-8")
					#print authorsRaw
					if j == 0:	
						authors = authorsRaw
					else:
						authors = authors + ", " + authorsRaw
			except: 
				cantidadAutores = "No authors"	


			metadata = authors + " - " + publicationTitle + ", " + publicationYear

			response[i] = {
				"title" : title,
				"url": url,
				"pdf": False,
				"abstract": "No abstract available",
				"metadata": metadata,
				}

		data = json.dumps(response, indent=4, sort_keys=True)	
	else:
		data = json.dumps(response, indent=4, sort_keys=True)

	#print data

	return data


def springerAPI(query):
	url = 'https://link.springer.com/search?&query=' + query + '&facet-content-type="ConferencePaper"&showAll=true'
	req = requests.get(url)
	statusCode = req.status_code
	

	response = {}
	html = BeautifulSoup(req.text, "html.parser")
	ol = html.find('ol', {'class': 'content-item-list'})

	if ol is not None:
		li = ol.findAll('li')

		print "LIIIII"
		print li

		i = 0

		for result in li:
			print result

			link = result.find('a', {'class': 'title'})
			print link

			if link is not None:
				url = "https://link.springer.com" + link['href']
				print url
				title = link.text.encode('utf8')
				abstract = result.find('p', {'class': 'snippet'}).text.encode('utf8').strip()
				metaRaw = result.find('p', {'class': 'meta'})

				authors = metaRaw.find('span', {'class': 'authors'})
				enumeration = metaRaw.find('a', {'class': 'publication-title'}).text.encode('utf8')
				
				if authors is not None:
					metadataAuthors = authors.findAll('a')
					metadata = ""
					for link in metadataAuthors:
						rawText = link.text.encode('utf8')
						metadata = metadata + rawText + ", "
					metadata = metadata[:-2] #quito la ultima coma de los autores
					metadata = metadata + " in " + enumeration
				else:
					metadata = enumeration

				response[i] = {
					"title" : title,
					"url": url,
					"pdf": False,
					"abstract": abstract,
					"metadata": metadata,
					}

				i += 1

	data = json.dumps(response, indent=4, sort_keys=True)	

	#print data

	return data


def searchAPI(query):

	science_dict = json.loads(scienceDirectAPI(query))
	xplore_dict = json.loads(ieeeXploreAPI(query))
	springer_dict = json.loads(springerAPI(query))

	response = {}

	i = 0

	for key in science_dict:
		title = science_dict[key]['title'].encode('utf8')
		print "Title: " + title
		url = science_dict[key]['url'].encode('utf8')
		print "url: " + url
		pdf = science_dict[key]['pdf']
		metadata = science_dict[key]['metadata'].encode('utf8')
		abstract = science_dict[key]['abstract'].encode('utf8')

		response[i] = {
				"title" : title,
				"url": url,
				"pdf": pdf,
				"abstract": abstract,
				"metadata": metadata,
			}

		i += 1

	for key in xplore_dict:
		title = xplore_dict[key]['title'].encode('utf8')
		print "Title: " + title
		url = xplore_dict[key]['url'].encode('utf8')
		print "url: " + url
		pdf = xplore_dict[key]['pdf']
		metadata = xplore_dict[key]['metadata'].encode('utf8')
		abstract = xplore_dict[key]['abstract'].encode('utf8')

		response[i] = {
				"title" : title,
				"url": url,
				"pdf": pdf,
				"abstract": abstract,
				"metadata": metadata,
			}

		i += 1

	for key in springer_dict:
		title = springer_dict[key]['title'].encode('utf8')
		print "Title: " + title
		url = springer_dict[key]['url'].encode('utf8')
		print "url: " + url
		pdf = springer_dict[key]['pdf']
		metadata = springer_dict[key]['metadata'].encode('utf8')
		abstract = springer_dict[key]['abstract'].encode('utf8')

		response[i] = {
				"title" : title,
				"url": url,
				"pdf": pdf,
				"abstract": abstract,
				"metadata": metadata,
			}

		i += 1

	data = json.dumps(response, ensure_ascii=False)

	print data

	"""
	with open('json/'+query+'.json', 'w') as file:
                json.dump(data, file)

	"""

	with io.open('json_raws/'+query+'.json', 'w', encoding='utf-8') as f:
		f.write(unicode(data))

	return data




def springer_articleAPI(url):

	pdf = False # springer no tiene pdfs
	req = requests.get(url)
	statusCode = req.status_code
	html = BeautifulSoup(req.text, "html.parser")

	now = datetime.now()

	print now

	with io.open('logs/'+str(now)[-5:]+'-springer.html', 'w', encoding='utf-8') as f:
		f.write(unicode(html))

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

	metadata = ""
	keywordsRaw = html.findAll('span', {'class': 'Keyword'})

	if(keywordsRaw != None):
		for i in range(len(keywordsRaw)):
			if i == 0:
				metadata = keywordsRaw[i].text[:-1] # Se borra el ultimo espacio.
			else:
				metadata = metadata + "; " + keywordsRaw[i].text[:-1]
	else:
		metadata = "Metadata is not available"


	pdf = html.find('a', {'class': 'gtm-pdf-link'})
	if(pdf != None):
		pdf = "https://link.springer.com" + pdf['href']
	else:
		pdf = False

	response = {
				"title" : title,
				"url": url,
				"pdf": pdf,
				"abstract": abstract,
				"metadata": metadata,
			}

	data = json.dumps(response, ensure_ascii=False)

	with io.open('json_raws/'+str(now)[-5:]+'-springer.html', 'w', encoding='utf-8') as f:
		f.write(unicode(data))

	#resultado = Resultado(0, title, url, pdf, abstract, metadata, False, False)

	return data






def ieeeXplore_articleAPI(url):

	pdf = False
	articleNumber = url.split("/")[4] # el elemento en la posicion 4 del link si se splitea en / es el articleNumber 

	headers = {
				'User-Agent':'BeautifulSoup, contact me at andresfilosok@gmail.com', 
				'Referer': 'https://ieeexplore.ieee.org/document/' + articleNumber,
				'Content-type': 'application/json'
	}

	urlSnippet = "https://ieeexplore.ieee.org/rest/document/" + articleNumber + "/snippet"
	req = requests.get(urlSnippet, headers=headers)
	statusCode = req.status_code
	html = BeautifulSoup(req.text, "html.parser")

	now = datetime.now()

	print now

	with io.open('logs/'+str(now)[-5:]+'-ieee.html', 'w', encoding='utf-8') as f:
		f.write(unicode(html))

	introduction = html.find('h3')
	snippet = html.find('p')

	if (introduction != None):
		introduction = introduction.text
	else:
		introduction = ""

	if (snippet != None):
		snippet = snippet.text
	else:
		snippet = "No abstract available"

	abstract = str(introduction + snippet)

	print abstract.encode('utf8')

	urlSimilar = "https://ieeexplore.ieee.org/rest/document/" + articleNumber + "/similar"
	req = requests.get(urlSimilar, headers=headers)
	json_data = req.text
	item_dict = json.loads(json_data)

	title = item_dict['title']

	url = "https://ieeexplore.ieee.org/document/" + articleNumber

	metadata = "Metadata is not available" # issue

	response = {
				"title" : title,
				"url": url,
				"pdf": pdf,
				"abstract": abstract,
				"metadata": metadata,
			}

	data = json.dumps(response, ensure_ascii=False)

	with io.open('json_raws/'+str(now)[-5:]+'-xplore.html', 'w', encoding='utf-8') as f:
		f.write(unicode(data))
 	
	#resultado = Resultado(0, title, url, pdf, snippet, metadata, False, False)

	return data



def scienceDirect_articleAPI(url):

	# URL Example 		
	# https://www.sciencedirect.com/science/article/pii/S0185269813718221
	# 1       2                     3       4       5   6
	pii = url.split("/")[6]

	# API Example
	# https://api.elsevier.com/content/article/pii/S0185269813718221?apiKey=3491fbfd6948a9e127f3ccf8eed94e2c

	print pii

	api_url = 'https://api.elsevier.com/content/article/pii/'+pii+'?apiKey=3491fbfd6948a9e127f3ccf8eed94e2c'
	headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8', 'Accept': 'application/json'}
	r = requests.get(api_url, headers=headers).json()

	results = json.dumps(r, indent=4, sort_keys=True)

	#print results

	data = json.loads(results)

	now = datetime.now()

	#print now

	with io.open('logs/'+str(now)[-5:]+'-science.html', 'w', encoding='utf-8') as f:
		f.write(unicode(results))

	try:
		title = data['full-text-retrieval-response']['coredata']['dc:title']
		title = title.split("1 1")[0] # Esto es porque a veces el titulo puede venir con una referencia (1 1). Solamente tomo la primera parte
	except:
		try: title = data['full-text-retrieval-response']['coredata']['pubType']
		except: title = "No title available"

	try: 
		print "Voy a ir a buscar el abstract"
		abstract = data['full-text-retrieval-response']['coredata']['dc:description'].encode('utf8').strip()
		abstract = abstract.replace("ÔÇö", "-")
		print "Encontre abstract: " + abstract.encode('utf8')
	except: 
		abstract = "No abstract available"

	if abstract == None:
		print "No hay abstract. Se esta yendo a buscar el texto original"
		try: 
			abstract = data['full-text-retrieval-response']['originalText'].split(title)[2] # Esto es porque si el texto original tiene mucha informacion basura 
			#print abstract.encode('utf8')																	# y cuando aparece el titulo de del articulo comienza un psudo abstract
		except IndexError: 																	# En caso de que (2) arroje una excepcion por index out of range se intenta
			abstract = data['full-text-retrieval-response']['originalText'].split(title)[1] # capturar el primer item del split. Esta funcionalidad es a modo de prueba.
			#print abstract.encode('utf8')																
		except:
			abstract = "No abstract available" 
	
	metadata = ""
	
	try: 
		keywordsRaw = data['full-text-retrieval-response']['coredata']['dcterms:subject'] # Dict of keywords

		#print keywordsRaw

		cantidadKeywords = len(keywordsRaw)/2

		for i in range (cantidadKeywords):
			if i == 0:
				metadata = keywordsRaw[i]['$']
				#print metadatakeywords
			else:
				metadata = metadata + "; " + keywordsRaw[i]['$']
				#print keywords
	except: 
		metadata = "Metadata not available"


	try: pdf = data['full-text-retrieval-response']['coredata']['openaccessArticle'] # True o False
	except: pdf = "False"

	print "Voy a armar el articulo"
	print "El abstract es este: "
	print abstract.encode('utf8')

	response = {
				"title" : title,
				"url": url,
				"pdf": pdf,
				"abstract": abstract,
				"metadata": metadata,
			}

	data = json.dumps(response, ensure_ascii=False)

	with io.open('json_raws/'+str(now)[-5:]+'-science.html', 'w', encoding='utf-8') as f:
		f.write(unicode(data))

	#resultado = Resultado(0, title, url, pdf, abstract, keywords, False, False)

	return data