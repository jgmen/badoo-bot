
FROM mcr.microsoft.com/playwright/python:v1.52.0-noble

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY requirements-dev.txt ./
RUN pip install -r requirements-dev.txt

COPY . .

EXPOSE 3000

CMD ["python", "src/main.py"]
