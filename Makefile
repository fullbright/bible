HOST=127.0.0.1
TEST_PATH=./
PROJECTPATH=$PWD

clean-pyc:
	find . -name 'processors/*.pyc' -exec rm --force {} +
	find . -name 'processors/*.pyo' -exec rm --force {} +
	name 'processors/*~' -exec rm --force  {}
	
clean-tex:
	for n in bible_fra/*.tex; do printf '%s\n' "$n"; done
	rm -i $(project).log; rm -i $(project).idx; rm -i $(project).lof; \
	rm -i $(project).out; rm -i $(project).pdf; rm -i $(project).toc; \
	rm -i $(project).aux; rm -i $(project).lot 

clean-build:
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive *.egg-info

install:
	sudo apt-get install texlive-bibtex-extra biber

generate-books:
	cd $(PWD)/bible_fra; python xml2latex.py; cd ..;
	

build-pdf-dev:
	for i in `seq 1 10`; do pdflatex -interaction=nonstopmode  bible_fra_tufte.tex ; done;

build-pdf-prd:
	for i in `seq 1 10`; do pdflatex -interaction=nonstopmode  bible_fra_tufte_full.tex ; done;

build-tex: generate-books
	pdflatex bible_fra_tufte.tex

build:
	echo "Compiling project $(project)"
	pdflatex -interaction=nonstopmode $(project).tex
	biber $(project)
	pdflatex -interaction=nonstopmode $(project).tex
	pdflatex -interaction=nonstopmode $(project).tex

extract_cross_ref:
	grep -oP '^[0-9a-zA-Z]{3,4}' bible_fra/resources/others/cross_references.txt | uniq > bible_fra/resources/others/uniq_book_shortcodes.txt

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

docker-run: docker-build
	docker run \
      --detach=false \
      --name=bible-builder \
      --publish=$(HOST):8080 \
      fullbright/bible-builder

docker-build:
	docker build \
      --file=./Dockerfile \
      --tag=fullbright/bible-builder ./