FROM python:3.10

RUN apt-get update


COPY requirements.txt ./
COPY files /home

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["tail", "-f", "/dev/null"]
