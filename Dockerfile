FROM python:3.9

COPY . /twstock

WORKDIR /twstock

RUN pip install -r requirements.txt

CMD ["python", "run.py"]
