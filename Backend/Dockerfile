FROM python:3.13-slim

WORKDIR /app

COPY Backend/pyproject.toml Backend/poetry.lock* ./
RUN pip install poetry
RUN poetry install --no-root

COPY Backend/backend ./backend

EXPOSE 5001

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "5001", "--reload"]
