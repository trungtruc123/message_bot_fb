# Basic Flask App run in heroku
$ heroku login

$ heroku git:clone -a truc301297

$ cd truc301297

$ git add .

$ git commit -am "make it better"

$ git push heroku master


# 1. Procfile: (use run in heroku: careful)
web: gunicorn app:app