FROM debian:jessie
MAINTAINER full3right [at] gmail [dot] com

RUN apt-get -qq update && \
	apt-get install -y --no-install-recommends texlive-fonts-recommended \
	texlive-latex-extra texlive-fonts-extra texlive-latex-base dvipng \
	texlive-latex-recommended texlive-bibtex-extra biber && \
	rm -rf /var/lib/apt/lists/*

RUN mkdir /myApp

CMD ["./build-bible.sh"]