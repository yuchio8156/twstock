FROM python:3.9

RUN apt-get clean && apt-get update && apt-get install -y locales

RUN locale-gen en_US.UTF-8

COPY . /twstock

WORKDIR /twstock

RUN pip install -r requirements.txt

CMD ["python", "run.py"]
