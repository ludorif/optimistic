FROM python:3

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY .. .

EXPOSE 5001

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "5001", "--reload"]
