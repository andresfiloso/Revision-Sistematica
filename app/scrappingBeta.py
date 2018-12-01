# -*- coding: utf-8 -*-
from flask import session, json
from bs4 import BeautifulSoup
import requests
import re
import io
from models import *

import time


import sys
reload(sys)
sys.setdefaultencoding('utf8')

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

