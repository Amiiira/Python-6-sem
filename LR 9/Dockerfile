FROM python:3.9-slim

RUN pip install fastapi uvicorn sqlalchemy psycopg2-binary

WORKDIR /project

COPY ./project /project

CMD ["uvicorn", "main:project", "--host", "0.0.0.0", "--port", "80"]
