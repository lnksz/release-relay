FROM fedora

WORKDIR /app

RUN dnf install -y \
    fedora-messaging \
    python3-pip \
    && dnf clean all

RUN pip3 install \
    pymsteams

ADD https://raw.githubusercontent.com/fedora-infra/fedora-messaging/stable/configs/fedora-key.pem /app/fedora-key.pem
ADD https://raw.githubusercontent.com/fedora-infra/fedora-messaging/stable/configs/fedora-cert.pem /app/fedora-cert.pem
ADD https://raw.githubusercontent.com/fedora-infra/fedora-messaging/stable/configs/cacert.pem /app/cacert.pem

COPY main.py /app/main.py
COPY relayconf.toml /app/relayconf.toml
COPY projects.toml /app/projects.toml

ENV FEDORA_MESSAGING_CONF=/app/relayconf.toml
ENV PROJECTS=/app/projects.toml

CMD [ "python3", "main.py" ]
