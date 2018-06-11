FROM jupyter/base-notebook
MAINTAINER Jan Kumor <elohhim@gmail.com>
LABEL Description="Docker image that contains Jupyter with a pre-compiled version of igraph's Python interface"
USER root
RUN apt-get -y update
RUN apt-get -y install build-essential libxml2-dev zlib1g-dev python-dev python-pip pkg-config libffi-dev libcairo-dev graphviz
RUN apt-get -y install texlive texlive-latex-extra vim aspell
RUN pip install --upgrade pip
RUN pip install python-igraph numpy matplotlib cairocffi
USER jovyan
