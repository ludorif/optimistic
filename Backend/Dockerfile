FROM python:3

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY . /app
WORKDIR /app

COPY .. .

CMD [ "python", "-m" , "flask", "--app", "Main", "run", "--debug", "--host=0.0.0.0"]
