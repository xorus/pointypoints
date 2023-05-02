FROM python:3.11

RUN pip install poetry==1.4.2 && \
    poetry config virtualenvs.create false

#RUN apt update && apt install -y <PACKAGE>\ <Package>
#RUN apt-get clean && \ rm -rf /var/lib/apt/lists/*

COPY . /app

WORKDIR /app
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN poetry lock && poetry install --only main

EXPOSE 8000

ENTRYPOINT ["/app/docker/init.sh"]
