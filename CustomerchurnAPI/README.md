# Author Ibrahim Koné 
# Image Classification Restful Api

An Image Classification Restful Api .

<br />

## How to use it

```bash
$ # Get the code
$ git clone https://github.com/Ibmaria/Image-Classification-Web-Apps.git
$ cd Image-Classification-Web-Apps/ImageRestApi
$
$ # Virtualenv modules installation (Unix based systems)
$ virtualenv env
$ source env/bin/activate
$
$ # Virtualenv modules installation (Windows based systems)
$ # virtualenv env
$ # .\env\Scripts\activate
$
$ # Install modules - SQLite Storage
$ pip3 install -r requirements.txt or pip install -r requirements.txt
$
$ # Create tables
$ python manage.py makemigrations
$ python manage.py migrate
$
$ # Start the application (development mode)
$ python manage.py runserver # default port 8000
$
$ # Start the app - custom port
$ # python manage.py runserver 0.0.0.0:<your_port>
$
$ # Access the web app in browser: http://127.0.0.1:5000/
```

```bash
$ # Get the code
$ git clone https://github.com/Ibmaria/Image-Classification-Web-Apps.git
$ cd Image-Classification-Web-Apps/ImageRestApi
$
$ # WITH DOCKER
$ docker-compose build
$ docker-compose up
$
$
$ # Access the web api in browser: http://127.0.0.1:5000/ and make requests
```



<br />


## Download Video App Here
![App Video](https://github.com/Ibmaria/Image-Classification-Web-Apps/blob/master/ImageRestApi/videoapp.gif)


## Codebase structure

The project is coded using a simple and intuitive structure presented below:

```bash
< PROJECT ROOT >
   |
   |-- app_docker.py/                              
   |--app.py
   |--classify_image.py  
   |--docker-compose.yml                      
   |--Dockerfile              
   |--requirements.txt
   |--requirements_docker.txt  
   |--INCEPTION.h5
   |--videoapp.gif
   |--videoapp.mp4
   |
   |-- ************************************************************************
```

<br />





