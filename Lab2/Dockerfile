FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get install -y iputils-ping

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY main.py .

ENTRYPOINT [ "python3", "main.py"]