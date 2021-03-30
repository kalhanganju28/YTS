# YoutubePlaylist_TO_SpotifyPlaylist
A simple python script that generates a Spotify playlist based on the song available in a specific Youtube playlist.

## Table of Contents
* [Technologies](#Technologies)
* [Setup](#Setup)
* [KeyPoints](#KeyPoints)

## Technologies
* [Youtube Data API v3]
* [Spotify Web API]
* [Requests Library v 2.22.0]
* [Youtube_dl v 2020.01.24]

## Setup
1) Navigate to the folder with the python file using `cd` command and Install All Dependencies using the below command: 
`pip install -r requirements.txt`
    * Wait for it to completely install all the libraries.

2) Make sure you have logged into both Youtube and Spotify before proceeding with the next step.

3) Collect You Spotify User ID and Oauth Token From Spotfiy and add it to secrets.py file
    * To Collect your User ID (**spotify_user_id**), go here: https://www.spotify.com/us/account/overview/ , copy your **Username** and paste it in **secrets.py** file
    * To Collect your Oauth Token (**spotify_token**), go here: https://developer.spotify.com/console/post-playlists/ and click the **GET TOKEN** button. Once generated, copy the token and paste it in **secrets.py** file.

4) Enable Oauth For Youtube and download the client_secrets.json   
    * Make sure you are logged into your Google Account
    * Go to : https://console.cloud.google.com/
    * Create a **New Project** and enter a **Project Name**
    * In the Project dashboard, in APIs card, click on **Go to APIs overview** at the bottom of the card
    * Click on **+ ENABLE APIS AND SERVICES**, search for **YouTube Data API v3** and click on blue **Enable** button.
    * Once Enabled, go to Credentials from the left Menu, click on **+ CREATE CREDENTIALS** and select **OAuth client ID**
    * In the Application Type drop down, select **Desktop app**. In Name, keep the same name or change the name according to your need. Then click **Create**
    * OAuth client created pop up will come with your client ID and client secret. Dont't copy these, just click ok. In the **OAuth 2.0 Client IDs** section in the credentials, you will see a download button in the end. Download this JSON, keep the name as **client_secret.json** and save it in the same folder where **create_playlist.py** file is present.
    * Now go to **OAuth consent screen**
    * Choose **External** and click Create.
    NOTE : Here onwards, make sure you use the same Gmail ID wherever it is asked.
    * Fill all the mandatory fields and click on **SAVE AND CONTINUE**
    * In the Scopes section, don't fill anything. Just click on **SAVE AND CONTINUE**
    * In the Test Users section, click on Add User and enter same Gmail ID as in previous steps. Once added, click on **SAVE AND CONTINUE**
    * In the Summary section, click on **BACK TO DASHBOARD** at the end.
    * With this, your youtube Data API is now fully configured.

5) We will have to make some changes in **create_playlist.py**
    * We will have to modify `playlist_id`, `playlist_name` and `playlist_description` at line number `18`, `21` and `24` respectively.
    * To get the the `playlist_id`, go to youtube (make sure you are logged in), go to your playlist and copy the code after `https://www.youtube.com/playlist?list=`. The long code, usually starting with `PL`, is your `playlist_id`.
    * `playlist_name` and `playlist_description` represents your Spotify playlists name and description. So, you can give anything name and description you want there.
    * Once these 3 changes are done, move to step 6.

6) Now we will run the file
    * Open cmd and Navigate to the folder with the python file using `cd` command
    * Run the File `python create_playlist.py`   
    * you'll immediately see `Please visit this URL to authorize this application: <some long url>`
    * click on it and log into your Google Account, copy the `authorization code` and paste it back in the cmd.
    * You will see the SongName, it's respective Artist and it's respective spotify_id in the output.
    ^ Once done, go to your spotify account and check playlist section. 

## KeyPoints
* Spotify Oauth token expires in 10-15 mins, If you come across a `KeyError` or if the code behaves improperly, this could be caused by an expired token. So just refer back to step 3 in local setup, generate a new token and copy the new `spotify_token` in `secrets.py` file. Your `spotify_user_id` will remain the same.

* Youtube Oauth token once created and enabled, will never have to be created again. Just make sure that you disable the youtube data API if you are not using it.
