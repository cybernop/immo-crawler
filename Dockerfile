FROM python:3.7

WORKDIR /crawler

COPY inout/ inout/
COPY provider/ provider/
COPY crawler.py .
COPY googlemaps.py .
COPY main.py .
COPY notifier.py .
COPY requirements.txt .

RUN pip install -r requirements.txt
RUN mkdir /data /cfg

ENTRYPOINT ["python", "main.py", "--data-dir", "/data", "--config", "/cfg/config.yml"]
