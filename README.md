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

- `Python` (>= 3.4 recommended) <https://www.python.org/>
- An `Actions Console Project`<https://console.actions.google.com/>
- A `Google account`<https://myaccount.google.com/>
- Google cloud SQL

# Setup

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

- Follow the steps to `configure the Actions Console project and the Google account <httpsb://>`.
- Follow the steps to `register a new device model and download the client secrets file <https://>`.
- Generate device credentials using ``google-oauthlib-tool``:

    pip install --upgrade google-auth-oauthlib[tool]
    google-oauthlib-tool --client-secrets path/to/client_secret_<client-id>.json --scope https://www.googleapis.com/auth/assistant-sdk-prototype --save --headless


# Run the samples

- Install the sample dependencies::

        sudo apt-get install portaudio19-dev libffi-dev libssl-dev
    
    
        pip install --upgrade -r requirements.txt

-  Verify audio setup::

        # Record a 5 sec sample and play it back
    
        python -m audio_helpers

- Run the push to talk sample. The sample records a voice query after a key press and plays back the Google Assistant's answer::

        python -m pushtotalk --device-id 'my-device-identifier' --device-model-id 'my-model-identifier'

- Try some Google Assistant voice query like "What time is it?" or "Who am I?".

- Try a device action query like "Turn on".

- Run in verbose mode to see the gRPC communication with the Google Assistant API::

    `python -m pushtotalk --device-id 'my-device-identifier' --device-model-id 'my-model-identifier' -v

- Send a pre-recorded request to the Assistant::

        python -m pushtotalk --device-id 'my-device-identifier' --device-model-id 'my-model-identifier' -i in.wav

- Save the Assistant response to a file::

        python -m pushtotalk --device-id 'my-device-identifier' --device-model-id 'my-model-identifier' -o out.wav

- Send text requests to the Assistant::

        python -m textinput --device-id 'my-device-identifier' --device-model-id 'my-model-identifier'

- Send a request to the Assistant from a local audio file and write the Assistant audio response to another file::

        python -m audiofileinput --device-id 'my-device-identifier' --device-model-id 'my-model-identifier' -i in.wav -o out.wav


# Troubleshooting

- Verify ALSA setup::

        # Play a test sound
    
        speaker-test -t wav
    

        # Record and play back some audio using ALSA command-line tools
    
        arecord --format=S16_LE --duration=5 --rate=16000 --file-type=raw out.raw
    
        aplay --format=S16_LE --rate=16000 --file-type=raw out.raw
    

- If Assistant audio is choppy, try adjusting the sound device's block size::

        # If using a USB speaker or dedicated soundcard, set block size to "0"
    
        # to automatically adjust the buffer size
    
        python -m audio_helpers --audio-block-size=0
    

        # If using the line-out 3.5mm audio jack on the device, set block size
    
        # to a value larger than the `ConverseResponse` audio payload size
    
        python -m audio_helpers --audio-block-size=3200
    

        # Run the Assistant sample using the best block size value found above
    
        python -m pushtotalk --audio-block-size=value

- If Assistant audio is truncated, try adjusting the sound device's flush size::

        # Set flush size to a value larger than the audio block size. You can
    
        # run the sample using the --audio-flush-size flag as well.
    
        python -m audio_helpers --audio-block-size=3200 --audio-flush-size=6400

See also the `troubleshooting section <https://developers.google.com/assistant/sdk/guides/service/troubleshooting>`_ of the official documentation.


# Sphinx Documents 

The contents are followed as:
  
- Smart Library IoT application
   
        - Console menu- based systems on RP & MP
   
        - Register and Login
   
         - Sockets sent from RP
   
                    - Search a book
   
                   -  Borrow a book
   
                   -  Return a book
  
- Web dashboard
   
         - Admin features and RESTful API
   
         - Generate CLOUD data visualisation report
   
         - visual representation of the all book lending and return statistics
  
  -Facial Recognition
   
         - OpenCV Based recognition
   
         - Images Stored function
  
- Challenging part
   
         - Voice/search feature
   
         - Object-detection feature
   
         - Unit test suite

