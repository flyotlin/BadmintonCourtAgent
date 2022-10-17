FROM python:3.8

WORKDIR /src

COPY requirements.txt .

RUN python3 -m pip install --upgrade pip && pip install -r requirements.txt

COPY . .
