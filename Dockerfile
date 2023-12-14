FROM python:3.12-slim as build

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt-get -y install build-essential

COPY requirements.txt install.py ./

RUN pip install --upgrade pip && \
    pip install --no-warn-script-location --user -r requirements.txt

ENV PATH=/root/.local/bin:$PATH

FROM python:3.12-slim

WORKDIR /app

ENV PATH=/root/.local/bin:$PATH

COPY --from=build /root/.local /root/.local

COPY . .

EXPOSE 9025

CMD [ "python3","-m","src.main" ]

