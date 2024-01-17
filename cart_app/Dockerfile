FROM python:3.11


COPY . .

RUN pip install poetry==1.7.1 && poetry config virtualenvs.create false && poetry update

