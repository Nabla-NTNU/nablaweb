MA = python manage.py 
.PHONY:
all:
	pip install -r requirements.txt
	$(MA) migrate
.PHONY:
content:
	pip install -U git+https://bitbucket.org/webkom/content-app.git

.PHONY:
run:
	$(MA) runserver 1337
.PHONY:
seed:
	$(MA) seed 
