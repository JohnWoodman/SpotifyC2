# SpotifyC2
Command and Control functionality using Spotify.
## How It Works
### genAcrostic.py
Commands are sent to the infected computer by creating an acrostic of the command with spotify songs (using the json files in /songs) and creates a playlist with the acrostic.
### backdoor.py
Command output is base64 encoded and embedded in the description of the playlist that contained the acrostic command (as well as creating other playlists as needed if the base64 encoded output exceeds the description size limit [300 characters]).
### getOutput.py
Retrieves and decodes the base64 encoded output from the playlist description, as well as deletes the playlists (technically unfollows the playlists as Spotify never actually deletes them)
