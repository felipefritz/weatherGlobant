# weatherGlobant

INSTRUCTIONS:
Install git and python in your machine

1.- Select a folder in your local machine, then run: git clone https://github.com/felipefritz/weatherGlobant.git
2.- Create a new python Virtual environment
3.- activate the virtual environment: venv/Scripts/activate ( or the name of the folder of your virtual environment folder)
3.- In terminal use: cd proyectoGlobant
4.- Execute the following command:  pip install -r requirements.txt
5.- Execute the following command: python manage.py migrate
6.- Finally execute: python manage.py runserver

7.- Go to: http://127.0.0.1:8000/api/weather/?city=$city&country=$country

API Parameters:
city=  is a string. Example: Valledupar
country= is a country code of two characters in lowercase. Example: co

Example of usage: 
  http://127.0.0.1:8000/api/weather/?city=santiago&country=cl
  
  
  
