FROM jupyter/base-notebook
MAINTAINER Jan Kumor <jan.kumor@gmail.com>
LABEL Description="Docker image that contains Jupyter with a pre-compiled version of igraph's Python interface"
USER root
RUN apt-get -y update && apt-get -y install build-essential libxml2-dev zlib1g-dev python-dev python-pip pkg-config libffi-dev libcairo-dev
RUN apt-get -y install graphviz
RUN pip install python-igraph
RUN pip install cairocffi
USER jovyan
