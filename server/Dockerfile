FROM python:3.10

RUN apt-get update
# && apt-get install -y 

COPY requirements.txt ./
COPY files /home

RUN pip install -r requirements.txt

CMD ["tail", "-f", "/dev/null"]
