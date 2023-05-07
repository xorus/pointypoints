FROM python:3.11

RUN pip install poetry==1.4.2 && \
    poetry config virtualenvs.create false

#RUN apt update && apt install -y <PACKAGE>\ <Package>
#RUN apt-get clean && \ rm -rf /var/lib/apt/lists/*

WORKDIR /app
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

COPY pyproject.toml /app
COPY poetry.lock /app
RUN poetry install --only main

COPY . /app
EXPOSE 8000

ENTRYPOINT ["/app/docker/init.sh"]
