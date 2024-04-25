# Release Relay

Relay release announcements of projects from https://release-monitoring.org/

Built on:

- Anitya: https://release-monitoring.org/static/docs/index.html
- Fedora Messaging: https://fedora-messaging.readthedocs.io/en/stable/
- MS Teams Webhooks: https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook

This is a small service, which listens to the Fedora Messaging bus for new release announcements of projects from release-monitoring.org. If a new release is announced, it will be relayed to a MS Teams channel.
A list of projects to listen to can be configured to only get the announcements for the projects, which are interesting for you.

## Usage

### Configuration

The configuration is done via environment variables:

- `FEDORA_MESSAGING_CONF`: Path to the [Fedora Messaging configuration file](https://fedora-messaging.readthedocs.io/en/stable/user-guide/quick-start.html#fedora-s-public-broker)
- `TEAMS_WEBHOOK` : The URL of the MS Teams webhook (secret)
- `PROJECTS` : path to a toml file with an array of the `projects`, which should be monitored:

```toml
projects = [
  "avahi",
  # Simple string of project name, if the project name is unambigous
  "bash",
  "bzip2",
  # Array of project name and homepage, if the name is ambigous
  ["openssl", "https://www.openssl.org"],
  "sudo",
]
```

[DataGrepper](https://apps.fedoraproject.org/datagrepper/raw?topic=org.release-monitoring.prod.anitya.project.version.update) can be used to get the name/homepage for your projects.


## Build

Even though there is a PyPI package for non fedora repos, it did through some random errors, so I use the fedora docker image.
And run the service as a container.


```sh
docker image build release-relay .
```

## Run

Configure your environment variable with the MS Teams webhook. You can either run a simple Docker command, use docker-compose or Portainer.

```sh
docker run --rm --name release-relay \
  -e TEAMS_WEBHOOK=https://outlook.office.com/webhook/... \
  release-relay
# or using the image from DockerHub
docker run --rm --name release-relay \
  -e TEAMS_WEBHOOK=https://outlook.office.com/webhook/... \
  efrgmbh/release-relay
```

## Internals

### Anitya Messages

The received messages in the python consumer are from the class `fedora_messaging.message.Message`.
And the actual message is a dict in the class `fedora_messaging.message.Message.body`.
There the `project` field is available on the top and both embedded into the `message` field.

Here a shortend example:

```
Id: f3ca7f44-f08e-48cc-aaeb-03af3fe01e6c
Topic: org.release-monitoring.prod.anitya.project.version.update
Headers: {
    "fedora_messaging_schema": "anitya.project.version.update",
    "fedora_messaging_severity": 20,
    "priority": 0,
    "sent-at": "2023-10-17T13:28:48+00:00",
    "x-received-from": [
        {
            "cluster-name": "rabbit@rabbitmq02.iad2.fedoraproject.org",
            "exchange": "amq.topic",
            "redelivered": false,
            "uri": "amqps://rabbitmq01.iad2.fedoraproject.org/%2Fpubsub"
        }
    ]
}
Body: {
    "distro": null,
    "message": {
        "agent": "anitya",
        "ecosystem": "rubygems",
        "odd_change": false,
        "old_version": "1.1.0",
        "packages": [],
        "project": {
            "backend": "Rubygems",
            "created_on": 1681242304.0,
            "ecosystem": "rubygems",
            "homepage": "https://rubygems.org/gems/neetodeploy/versions/0.1",
            "id": 339337,
            "name": "neetodeploy",
            "regex": null,
            "stable_versions": [
                "1.1.1",
                "1.1.0"
            ],
            "updated_on": 1697549327.0,
            "version": "1.1.1",
            "version_url": null,
            "versions": [
                "1.1.1",
                "1.1.0"
            ]
        },
        "stable_versions": [
            "1.1.1",
            "1.1.0"
        ],
        "upstream_version": "1.1.1",
        "versions": [
            "1.1.1",
            "1.1.0"
        ]
    },
    "project": {
        "backend": "Rubygems",
        "created_on": 1681242304.0,
        "ecosystem": "rubygems",
        "homepage": "https://rubygems.org/gems/neetodeploy/versions/0.1",
        "id": 339337,
        "name": "neetodeploy",
        "regex": null,
        "stable_versions": [
            "1.1.1",
            "1.1.0",
        ],
        "updated_on": 1697549327.0,
        "version": "1.1.1",
        "version_url": null,
        "versions": [
            "1.1.1",
            "1.1.0"
        ]
    }
}
```
