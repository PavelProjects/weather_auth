FROM ubuntu

RUN apt-get update
RUN apt-get install python3 python3-pip curl -y

COPY ./ /
RUN pip3 install -r /requirenments.txt
cmd python3 auth.py
expose 50051 8080
