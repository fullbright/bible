HOST=127.0.0.1
TEST_PATH=./
PROJECTPATH=$PWD

clean-pyc:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	name '*~' -exec rm --force  {}
	
clean-tex:
	for n in bible_fra/*.tex; do printf '%s\n' "$n"; done 

clean-build:
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive *.egg-info

install:
	sudo apt-get install texlive-bibtex-extra biber

build-tex:
	cd $(PWD)/bible_fra; python xml2latex.py; cd ..;
	pdflatex bible_fra_tufte.tex

build:
	echo "Compiling project $(project)"
	pdflatex $(project).tex
	biber $(project)
	pdflatex $(project).tex
	pdflatex $(project).tex

isort:
	sh -c "isort --skip-glob=.tox --recursive . "

lint:
	flake8 --exclude=.tox

test: clean-pyc
	py.test --verbose --color=yes $(TEST_PATH)

test-makefile:
	cat -e -t -v Makefile

run:
	python manage.py runserver

docker-run:
	docker build \
      --file=./Dockerfile \
      --tag=my_project ./
	docker run \
      --detach=false \
      --name=my_project \
      --publish=$(HOST):8080 \
      my_project
