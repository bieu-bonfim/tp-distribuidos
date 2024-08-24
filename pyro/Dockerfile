FROM python:3.10

COPY requirements.txt ./
RUN pip install -r requirements.txt

CMD ["python", "-m", "Pyro5.nameserver","-n", "cryptid_ns", "--host", "0.0.0.0", "--port", "8020"]