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

# Copying environments variables into /etc/environment for using them from cron
ENTRYPOINT ["/bin/sh", "-c", "printenv | awk -F= '{printf \"%s=\\\"%s\\\"\\n\",$1,$2}' | sed 's/\\\"\\\"/\\\"/g' | sort -u > /etc/environment && exec \"$0\" \"$@\"", "cron", "-f"]

CMD ["cron", "-f"]