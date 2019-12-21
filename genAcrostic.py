import json
import random 
import requests

genre = input("What genre would you like to acrostic with (rock seems to be the most reliable)? ")

command_in = input("\nEnter the command to be executed: ")

playlist_name = input("\nEnter playlist name (doesn't affect anything): ")

command_write =command_in

#Encode command
command_in = command_in.replace(" ", "space")
command_in = command_in.replace("-", "hiphen")
command_in = command_in.replace("/", "fslash")
command_in = command_in.replace("\\", "bslash")
command_in = command_in.replace("!", "ebang")
command_in = command_in.replace("#", "epound")
command_in = command_in.replace("$", "edollar")
command_in = command_in.replace("@", "eatsym")
command_in = command_in.replace("%", "eperc")
command_in = command_in.replace("^", "ecarr")
command_in = command_in.replace("&", "eand")
command_in = command_in.replace("*", "estar")
command_in = command_in.replace("(", "eopar")
command_in = command_in.replace(")", "ecpar")
command_in = command_in.replace("+", "eplus")
command_in = command_in.replace("=", "eeq")
command_in = command_in.replace(".", "edot")
command_in = command_in.replace(",", "ecoma")
command_in = command_in.replace("?", "eques")
command_in = command_in.replace("1", "eone")
command_in = command_in.replace("2", "etwo")
command_in = command_in.replace("3", "ethree")
command_in = command_in.replace("4", "efour")
command_in = command_in.replace("5", "efive")
command_in = command_in.replace("6", "esix")
command_in = command_in.replace("7", "eseven")
command_in = command_in.replace("8", "eeight")
command_in = command_in.replace("9", "enine")
command_in = command_in.replace("0", "ezero")

with open("songs/" + genre + ".js", "r") as read_file:
	data = json.load(read_file)

#Build acrostic for command and build uri list
title_final = []
title_uri = []
for c in command_in:
	track_arr = []
	for t in data:
		if (t["title"][0].lower() == c.lower()):
			track_arr.append(t)
	title_final.append(random.choice(track_arr))

uri_list = ''
print("\n##########Acrostic##########")
for item in title_final:
	print(item['title'])
	uri_list = uri_list + '"' + item['uri'] + '",'
print("############################\n")

uri_list = uri_list[:-1]

#Create playlist and add tracks from uri list
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

data = '{"name":"' + playlist_name + '","description":"blah","public":true}'

response = requests.post('https://api.spotify.com/v1/me/playlists', headers=headers, data=data)

if(response.status_code == 201):
	print("(+)Playlist Created!\n")

js_response = response.json()

playlist_id = js_response['id']

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + access_token,
}

data = '{"uris":[' + uri_list + ']}'

response = requests.post('https://api.spotify.com/v1/playlists/' + playlist_id + '/tracks', headers=headers, data=data)

if(response.status_code == 201):
	print("(+)Command Added to Playlist!\n")

#Append playlist id and commmand to file to be referenced by getOutput.py
f = open("playlist_id_list.txt", "a+")

f.write(playlist_id + "," + command_write + '\n')

f.close()

print("(+)Added playlist id to file!\n")








