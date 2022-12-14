from typing import Optional
from abc import ABC
import docker
import time


class DockerContainer(ABC):
    IMAGE: str = None
    COMMAND: str = None
    VOLUMES = {}
    PORTS = {}
    ENVIRONMENT = {}
    WAIT_SECONDS = 5

    def __init__(self):
        self.client = docker.from_env()
        self.container = None

    def run(self):
        if self.IMAGE is None:
            raise NotImplementedError

        self.container = self.client.containers.run(
            self.IMAGE,
            command=self.COMMAND,
            detach=True,
            volumes=self.VOLUMES,
            ports=self.PORTS,
            environment=self.ENVIRONMENT,
        )

        if self.WAIT_SECONDS:
            time.sleep(self.WAIT_SECONDS)

    def stop(self):
        if self.container is not None:
            self.container.stop()


class MosquittoContainer(DockerContainer):
    IMAGE = "eclipse-mosquitto:2.0"
    COMMAND = "mosquitto -c /mosquitto-no-auth.conf"
    PORTS = {1883: 1883}


class RedisContainer(DockerContainer):
    IMAGE = "redis"
    PORTS = {6379: 6379}


class MariaDBContainer(DockerContainer):
    IMAGE = "mariadb"
    PORTS = {3306: 3306}
    WAIT_SECONDS = 7
    ENVIRONMENT = {
        "MARIADB_USER": "user",
        "MARIADB_PASSWORD": "1234",
        "MARIADB_DATABASE": "main",
        "MARIADB_ROOT_PASSWORD": "0000",
    }


class MongoDBContainer(DockerContainer):
    IMAGE = "mongo"
    PORTS = {27017: 27017}
