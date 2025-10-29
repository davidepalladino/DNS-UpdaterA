FROM ghcr.io/astral-sh/uv:trixie-slim

LABEL authors="Davide Palladino"
LABEL descriptions="A Python script to automate updating DNS record A type."

COPY ./cron /etc/cron.d
RUN chown root:root -R /etc/cron.d && \
    chmod 0644 -R /etc/cron.d

COPY . /app
WORKDIR /app
RUN apt-get update && \
    apt-get install -y cron make && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf cron && \
    make install && make sync

CMD ["cron", "-f"]