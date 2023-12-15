FROM python:3.12-slim as build

ENV DEBIAN_FRONTEND noninteractive
WORKDIR /app
COPY requirements.txt ./

RUN pip install --upgrade pip && \
    pip install --no-warn-script-location --user -r requirements.txt

COPY . .

EXPOSE 9025

CMD [ "python3","-m","src.main" ]

