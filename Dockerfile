FROM python:3.10

COPY . .
WORKDIR .

RUN pip3 install -r requirements.txt
USER root
ENTRYPOINT ["python3","main.py"]
