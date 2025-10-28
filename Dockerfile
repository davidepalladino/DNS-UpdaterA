FROM ghcr.io/astral-sh/uv:trixie-slim

LABEL authors="Davide Palladino"
LABEL descriptions="A Python script to automate updating DNS record A type."

COPY ./cron /etc/cron.d/cron
RUN apt-get update && \
    apt-get install -y cron make && \
    rm -rf /var/lib/apt/lists/* && \
    chown root:root /etc/cron.d/cron && \
    chmod 0644 /etc/cron.d/cron

ADD . /app
WORKDIR /app
RUN make install && make sync

CMD ["cron", "-f"]