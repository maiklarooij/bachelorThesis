FROM python:3.11-bookworm

WORKDIR /app

COPY . .

RUN apt-get update -y
RUN apt-get install libsndfile1 -y
RUN pip install --no-cache-dir -r requirementsDocker.txt

EXPOSE 3012

CMD ["uvicorn", "appDocker:app", "--host", "0.0.0.0", "--port", "3012"]
