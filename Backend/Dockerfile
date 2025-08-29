FROM python:3.13-slim

WORKDIR /app

COPY Backend/requirements.txt .
RUN pip install --no-cache-dir -r ./requirements.txt

COPY Backend/backend ./backend

EXPOSE 5001

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "5001", "--reload"]
