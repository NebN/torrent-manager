# Torrent Manager

#### Python >=3.10

**manage.sh** assumes the presence of a venv folder in the project's root

    cd torrent-manager
    python -m venv venv
    pip install -r requirements.txt

-------------------------

#### Required configuration (root folder)

##### conf.ini

    [FOLDERS]
    # destination folder for TV shows
    tv = /some/path
    # destination folder for movies
    movies = /some/path

    [USERS]
    # unix group to chgrp when creating new directories, not mandatory
    group = somegroup

    [TELEGRAM]
    # bot api key to send error messages, not mandatory
    key = 123:ABC
    # chat id to send error messages to, not mandatory
    chat_id = 123

    [MOVIEDATABASE]
    # not used currently 
    key = 
    # not used currently
    read_access_token = 

