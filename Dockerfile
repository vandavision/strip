FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y wget && \
    wget -q https://github.com/stripe/stripe-cli/releases/download/v1.8.7/stripe_1.8.7_linux_x86_64.tar.gz && \
    tar -xvf stripe_1.8.7_linux_x86_64.tar.gz && \
    mv stripe /usr/local/bin/stripe

EXPOSE 5000

CMD ["python", "app.py"]
