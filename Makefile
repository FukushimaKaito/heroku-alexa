login:
	heroku login

setbuildpacks:
	heroku buildpacks:set heroku/python

prepare:
	heroku git:remote -a kateisaien-py

push:
	git push heroku master

log:
	heroku logs --tail
