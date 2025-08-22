FROM python:3

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY . /app
WORKDIR /app

ENV PATH=$PATH:/root/.local/bin

COPY .. .

EXPOSE 5001


CMD [ "fastapi", "dev", "backend/main.py", "--port", "5001", "--host=0.0.0.0"]
