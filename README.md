# SpotifyC2
Command and Control functionality using Spotify.
## How It Works
It sends the commands to the infected computer by creating an acrostic of the command with spotify songs and creates a playlist with the acrostic. 

Command output is base64 encoded and embedded in the description of the playlist that contained the acrostic command (as well as creating other playlists as needed if base64 encoded output is exceeds description size limit [300 characters]).
