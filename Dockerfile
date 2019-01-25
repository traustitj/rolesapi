FROM ubuntu:18.04
MAINTAINER traustitj@mac.com

RUN apt-get update
RUN apt-get install python3
WORKDIR /work
ADD . /work
RUN ["pip", "install", "-r", "requirements"]
RUN ["python", "setup.py"]
EXPOSE 5000
CMD ["python", "server.py"]