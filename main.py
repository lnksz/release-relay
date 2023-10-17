#!/usr/bin/env python3
from os import getenv
from fedora_messaging import api, config
import pymsteams

# tomllib is in std since 3.11
try:
    import tomllib
except ImportError:
    import toml as tomllib


def post_card(msg, projects):
    project = msg['project']['name']
    if project not in projects:
        print(f"Project {project} not in projects list, ignoring")
        return
    version = msg['project']['version']
    print(f"Project {project} released {version}!")
    card = pymsteams.connectorcard(getenv("TEAMS_WEBHOOK"))
    card.title(f"Project {project} released {version}!")
    card.summary(f"A new version of the project has been released {version}")
    card.send()


def message_callback(message):
    post_card(message.body, projects)


if __name__ == "__main__":
    if getenv("FEDORA_MESSAGING_CONF") is None:
        print("Please set the `FEDORA_MESSAGING_CONF` environment variable to the config file")
        exit(1)

    if getenv("TEAMS_WEBHOOK") is None:
        print("Please set the `TEAM_WEBHOOK` environment variable to the webhook URL")
        exit(1)

    if getenv("PROJECTS") is None:
        print("Please set the `PROJECTS` environment variable to the projects toml file")
        exit(1)

    config.conf.setup_logging()

    topics = []
    for binding in config.conf['bindings']:
        topics.extend(binding['routing_keys'])

    projects = []
    with open(getenv("PROJECTS"), 'rb') as f:
        projects = tomllib.load(f)['projects']

    print("Listening on topics {}".format(config.conf['bindings'][0]['routing_keys']))
    print("Acting on projects {}".format(projects))
    api.consume(message_callback)
