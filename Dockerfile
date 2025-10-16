# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
#RUN pip install --no-cache-dir -r requirements.txt
RUN pip3 install -r requirements.txt

#COPY . .

CMD [ "python3", "mcp_sql.py"]