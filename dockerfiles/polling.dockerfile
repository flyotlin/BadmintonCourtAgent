FROM python:3.8

WORKDIR /app

COPY requirements.txt .

RUN python3 -m pip install --upgrade pip && pip install -r requirements.txt

COPY . .

CMD ["python3", "polling_app.py"]
