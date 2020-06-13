import requests
import json

def buscadir(url, codpostal):
	dir = 'sin dir'
	response = requests.get(url + codpostal)
	if response.status_code == 200:
		response_json = json.loads(response.content)
		dir = response_json["provincia"] + ", " + response_json["canton"] + ", " + response_json["distrito"]	
	else:
		response_json = json.loads(response.content)
		dir = response_json["Error de codigo"]
	return(dir)

def listapro(url):
	prov = []
	response = requests.get(url)
	if response.status_code == 200:
		response_json = json.loads(response.content)
		for item in response_json:
			prov.append(item["nombre"])
	return(prov)

def codpro(url, nombre):
	prov = 'sin cod'
	response = requests.get(url)
	if response.status_code == 200:
		response_json = json.loads(response.content)
		prov = response_json["codigo"]
	return(prov)


'''
datos = {"cedula":ced}
	response = requests.post(url, json=datos)
	if response.status_code == 200:
		response_json = json.loads(response.content)
		dir = response_json["provincia"]		
	return(dir)
'''
