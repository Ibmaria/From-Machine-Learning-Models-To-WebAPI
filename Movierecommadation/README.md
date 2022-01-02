# Author Ibrahim Koné 
# Movie Recommadation  Django Web App



Every time I go to a movie, it’s magic, no matter what the movie’s about.Steven Spielberg
<br />

## How to use it

```bash
$ # Get the code
$ git clone https://github.com/Ibmaria/MovieRecommadationApp.git
$ cd MovieRecommadationApp
$
$ # Virtualenv modules installation (Unix based systems)
$ virtualenv env
$ source env/bin/activate
$
$ # Virtualenv modules installation (Windows based systems)
$ # virtualenv env
$ # .\env\Scripts\activate
$ #or with Anaconda
$ #conda create -n yourenvironementname
$ # activate yourenvironementname
$
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
$ # Access the web app in browser: http://127.0.0.1:8000/projets/movie/
```





<br />


## Download Video App Here
![App Video](https://github.com/Ibmaria/From-Machine-Learning-Models-To-WebAPI/blob/master/Movierecommadation/videoapp.gif)


## Codebase structure

The project is coded using a simple and intuitive structure presented below:

```bash
< PROJECT ROOT >
   |
   |-- movie/                              
   |--movierecommadation/
   |--Notebook/                                    
   |--requirements.txt
   |--manage.py
   |-- ************************************************************************
```

<br />





