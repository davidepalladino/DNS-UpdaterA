FROM ghcr.io/astral-sh/uv:trixie-slim

LABEL authors="Davide Palladino"
LABEL descriptions="A Python script to automate updating DNS record A type."

COPY ./cron /etc/cron.d
RUN apt-get update && \
    apt-get install -y cron make && \
    rm -rf /var/lib/apt/lists/* && \
    chown root:root -R /etc/cron.d && \
    chmod 0644 -R /etc/cron.d

ADD . /app
WORKDIR /app
RUN make install && make sync

CMD ["cron", "-f"]