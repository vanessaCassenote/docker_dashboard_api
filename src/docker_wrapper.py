''' This class manages docker containers '''

import logging
import docker
from docker.errors import APIError, ContainerError, ImageNotFound

logging.basicConfig(filename="log.log",format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("__name__")

client = docker.DockerClient(base_url='unix:///home/vanessac/.docker/desktop/docker.sock')

class DockerWrapper:
    ''' This class manages docker containers '''

    def __init__(self) -> None:
        self.client = client

    def list_images(self):
        ''' Get list of docker images '''
        try:
            images = self.client.images.list()
            logger.info("Retrieved list of docker images")
        except APIError as e:
            logger.exception("Could not retrieve docker images, error: %s", e)
        else:
            return images

    def list_containers(self, all_cont):
        ''' Get list of docker containers '''
        try:
            containers = self.client.containers.list(all=all_cont)
            logger.info("Retrieved list of docker containers")
        except APIError as e:
            logger.exception("Could not retrieve docker containers, error: %s", e)
        else:
            return containers

    @staticmethod
    def run_container(image):
        ''' Run a docker container '''
        try:
            container = client.containers.run(image, detach=True)
            logger.info("Container running %s",container.logs())
        except ContainerError as e:
            logger.exception("Container error: %s", e)
        except ImageNotFound as e:
            logger.exception("Image error: %s", e)
        except APIError as e:
            logger.exception("Server error: %s", e)
        else:
            return "Container running!"

    @staticmethod
    def stop_container(container):
        ''' Stop a docker container '''
        try:
            container = client.containers.get(container)
            container.stop()
            logger.info("Container stopped %s %s",container.id,container.status)
        except APIError as e:
            logger.exception("Server error: %s", e)
        else:
            return "Container stopped!"

    @staticmethod
    def start_container(container):
        ''' Start a docker container '''
        try:
            container = client.containers.get(container)
            container.start()
            logger.info("Container started %s %s",container.id,container.status)
        except APIError as e:
            logger.exception("Server error: %s", e)
        else:
            return "Container started!"

    @staticmethod
    def remove_container(container):
        ''' Remove a docker container if it is not running'''
        try:
            container = client.containers.get(container)
            if container.status == "running":
                return "This container is running, stop it before deleting!"
            container.remove()
            logger.info("Container removed %s",container.id)
        except APIError as e:
            logger.exception("Server error: %s", e)
        else:
            return "Container removed!"

    @staticmethod
    def restart_container(container):
        ''' Restart a docker container '''
        try:
            container = client.containers.get(container)
            container.restart()
            logger.info("Container restarted %s %s",container.id,container.status)
        except APIError as e:
            logger.exception("Server error: %s", e)
        else:
            return "Container restarted!"
