FROM python:3

WORKDIR /optimistic-docker

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "--app", "Main", "run", "--debug", "--host=0.0.0.0"]
