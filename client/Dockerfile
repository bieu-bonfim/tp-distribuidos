FROM python:3.10

RUN apt-get update && \
    apt-get install -y libgl1-mesa-dev libglu1-mesa-dev x11-apps && \
    rm -rf /var/lib/apt/lists/*


COPY requirements.txt ./
COPY files /home

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["tail", "-f", "/dev/null"]
