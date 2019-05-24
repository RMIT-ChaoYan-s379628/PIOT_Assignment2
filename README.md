# PIOT_Assignment2
This repository contains a reference sample for the PIOT_Assignment2 Python package.

The Library Management System (LMS)  should contacted to the local council library automatically and used to borrow, return and maintain the backend information. The two main types of users: library user and library admin.
The implementation of this assignment involves the following components for LMS (Library Management System):
- Python documentation tools such as Sphinx
- Unit testing in Python
- Socket Programming
- Writing own API using Python’s microframework Flask
- AI features such as facial recognition, object detection and Voice detection
- Programming with Cloud databases and,
- Selected Software Engineering Project Management/Tools


# Prerequisites
-------------

- `Python` (>= 3.4 recommended)
- An `Actions Console Project`
- A `Google account`<https://myaccount.google.com/>`_
- Google cloud SQL

# Setup
-----

- Install Python 3

    - Ubuntu/Debian GNU/Linux::

        sudo apt-get update
        
        sudo apt-get install python3 python3-venv

    - `MacOSX, Windows, Other`<https://www.python.org/downloads/>

- Create a new virtual environment (recommended)::

        python3 -m venv env
    
        env/bin/python -m pip install --upgrade pip setuptools wheel
    
        source env/bin/activate
    
    
        - sudo apt install sqlite3
    
        - sudo apt install default-libmysqlclient-dev 
    
        - sudo apt install mysql-client
    
        - sudo apt install python3-venv
    
        - pip3 install virtualenv
    
        - pip3 install flask sense-hat
    
        - pip3 install rtimulib
    
        - pip3 install python-dotenv
    
        - pip3 install google-api-python-client oauth2client 
    
        - pip3 install httplib2
    
        - pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
    
        - pip3 install pymysql
    
        - pip3 install tabulate
    
        - pip3 install sqlalchemy


# Authorization
-----

- Follow the steps to `configure the Actions Console project and the Google account <httpsb://>`_.
- Follow the steps to `register a new device model and download the client secrets file <https://>`_.
- Generate device credentials using ``google-oauthlib-tool``:

    pip install --upgrade google-auth-oauthlib[tool]
    google-oauthlib-tool --client-secrets path/to/client_secret_<client-id>.json --scope https://www.googleapis.com/auth/assistant-sdk-prototype --save --headless


# Run the samples

# Troubleshooting

# License
