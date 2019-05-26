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

- Raspberry model 3
- `Python` (>= 3.4 recommended) <https://www.python.org/>
- An `Actions Console Project`<https://console.actions.google.com/>
- A `Google account`<https://myaccount.google.com/>
- Google’s GCP IoT platform (Google Cloud Platform)


# Setup

- Install Python 3

    - Ubuntu/Debian GNU/Linux::

        sudo apt-get update
        
        sudo apt-get install python3 python3-venv
        
        sudo apt install sqlite3
    
        sudo apt install default-libmysqlclient-dev 
    
        sudo apt install mysql-client
        
        sudo apt install python3-venv
    
        pip3 install virtualenv
        
        pip3 install pymysql
    
        pip3 install tabulate
    
        pip3 install sqlalchemy
        
        pip3 install Flask-WTF
        
        pip3 install flask-bootstrap
        
        pip3 install Flask-HTTPAuth
        
        pip3 install Flask-SQLAlchemy
        
        pip3 install pyecharts

    - `MacOSX, Windows, Other`<https://www.python.org/downloads/>

- Create a new virtual environment (recommended):

        python3 -m venv env
    
        env/bin/python -m pip install --upgrade pip setuptools wheel
    
        source env/bin/activate
        
        - sudo apt-get install libtiff5-dev libtiff5 libjbig-dev
        
        - sudo apt-get install libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.5-dev tk8.5-dev python- tk
        
        - pip install wheel
        
        - pip3 install flask sense-hat
    
        - pip3 install rtimulib
    
        - pip3 install python-dotenv
    
        - pip3 install google-api-python-client oauth2client 
    
        - pip3 install httplib2
    
        - pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib   

- Install Open-CV :
        --- Installing OpenCV on Pi ---
        sudo apt-get purge wolfram-engine
        sudo apt-get purge libreoffice*
        sudo apt-get clean
        sudo apt-get autoremove

        sudo apt-get update && sudo apt-get upgrade

        sudo apt-get install build-essential cmake pkg-config
        sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
        sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
        sudo apt-get install libxvidcore-dev libx264-dev
        sudo apt-get install libgtk2.0-dev libgtk-3-dev
        sudo apt-get install libcanberra-gtk*
        sudo apt-get install libatlas-base-dev gfortran
        sudo apt-get install python2.7-dev python3-dev

        cd ~
        wget -O opencv.zip https://github.com/opencv/opencv/archive/3.3.0.zip
        unzip opencv.zip
        wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/3.3.0.zip
        unzip opencv_contrib.zip

        pip3 install numpy

        cd ~/opencv-3.3.0/
        mkdir build
        cd build
        cmake -D CMAKE_BUILD_TYPE=RELEASE \
        -D CMAKE_INSTALL_PREFIX=/usr/local \
        -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.3.0/modules \
        -D ENABLE_NEON=ON \
        -D ENABLE_VFPV3=ON \
        -D BUILD_TESTS=OFF \
        -D INSTALL_PYTHON_EXAMPLES=OFF \
        -D BUILD_EXAMPLES=OFF ..

        # Update CONF_SWAPSIZE to a larger size.
        sudo nano /etc/dphys-swapfile

        # set size to absolute value, leaving empty (default) then uses computed value
        #   you most likely don't want this, unless you have an special disk situation
        # CONF_SWAPSIZE=100
        CONF_SWAPSIZE=1024

        sudo /etc/init.d/dphys-swapfile restart

        make -j4

        sudo make install
        sudo ldconfig

        # Reset CONF_SWAPSIZE to a smaller size.
        sudo nano /etc/dphys-swapfile

        # set size to absolute value, leaving empty (default) then uses computed value
        #   you most likely don't want this, unless you have an special disk situation
        CONF_SWAPSIZE=100
        # CONF_SWAPSIZE=1024

        sudo /etc/init.d/dphys-swapfile restart

        cd /usr/local/lib/python3.5/dist-packages/

        sudo mv cv2.cpython-35m-arm-linux-gnueabihf.so cv2.so

        cd ~

        # Test OpenCV.
        python3

        >>> import cv2
        >>> cv2.__version__
        '3.3.0'
        >>> quit()

        --- Installing dlib and face_recognition python3 packages ---
        sudo apt-get install build-essential \
                cmake \
                gfortran \
                git \
                wget \
                curl \
                graphicsmagick \
                libgraphicsmagick1-dev \
                libatlas-dev \
                libavcodec-dev \
                libavformat-dev \
                libboost-all-dev \
                libgtk2.0-dev \
                libjpeg-dev \
                liblapack-dev \
                libswscale-dev \
                pkg-config \
                python3-dev \
                python3-numpy \
                python3-pip \
                zip

        sudo apt-get install python3-picamera

        pip3 install --upgrade picamera[array]

        # Update CONF_SWAPSIZE to a larger size.
        sudo nano /etc/dphys-swapfile

        # set size to absolute value, leaving empty (default) then uses computed value
        #   you most likely don't want this, unless you have an special disk situation
        # CONF_SWAPSIZE=100
        CONF_SWAPSIZE=1024

        sudo /etc/init.d/dphys-swapfile restart

        pip3 install dlib
        pip3 install face_recognition(cmake?)

        # Reset CONF_SWAPSIZE to a smaller size.
        sudo nano /etc/dphys-swapfile

        # set size to absolute value, leaving empty (default) then uses computed value
        #   you most likely don't want this, unless you have an special disk situation
        CONF_SWAPSIZE=100
        # CONF_SWAPSIZE=1024

        sudo /etc/init.d/dphys-swapfile restart

        --- Installing imutils python3 package ---

        pip3 install imutils

- Install QR Code :
        pip3 install pyzbar

- Install Google Speech Recognition :  
        pip3 install SpeechRecognition
        sudo apt-get install portaudio19-dev python-all-dev python3-all-dev pip3 install pyaudio
        pip3 install google-api-python-client
        sudo apt-get install flac

        cd ~
        sudo nano .asoundrc
        copy text:
                pcm.!default {
                type asym
                capture.pcm "mic" playback.pcm "speaker"
                } pcm.mic {
                type plug slave {
                pcm "hw:1,0" }
                } pcm.speaker {
                type plug slave {
                pcm "hw:0,0" }
                }
        save and exit


# Running 
- Run Master Pi

    cd PIOT_Assignment2
   
    python3 Master_Pi_socket.py
    
- Run Receive Pi in Vitural Environment
    
    cd PIOT_Assignment2
    
    source venv/bin/activate
    
    python3 Receive_Pi_socket.py


# Sphinx Documents 

The contents are followed as:
  
- Smart Library IoT application
   
         - Console menu- based systems on RP & MP
   
         - Register and Login
   
         - Sockets sent from RP
   
         - Search a book
   
         - Borrow a book
   
         - Return a book
  
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

