''' Flask API to manage docker containers '''

from flask import request
from app import app
from src.docker_wrapper import DockerWrapper

@app.route("/list_imgs", methods=["GET"])
def list_images():
    ''' List all docker images '''
    response = DockerWrapper().list_images()
    images = {}
    images["images"] = []
    for i in response:
        images["images"].append({"tags":i.tags, "id": i.id})
    return images

@app.route("/list_containers", methods=["POST"])
def list_containers():
    ''' List containers
        :param: when key 'all' is set to True all containers are shown
                when False only running containers are shown
    '''
    data = request.get_json()
    all_cont = data["all"] == "True"

    response = DockerWrapper().list_containers(all_cont)
    containers = {}
    containers["containers"] = []
    for i in response:
        containers["containers"].append({"name":i.name,
                                         "id": i.id, 
                                         "image":i.image.id, 
                                         "status":i.status})
    return containers

@app.route("/run_container", methods=["POST"])
def run_container():
    ''' Run container
        :param: "image" key receives imagem name
    '''
    data = request.get_json()
    image = data["image"]
    return DockerWrapper.run_container(image)

@app.route("/stop_container", methods=["POST"])
def stop_container():
    ''' Stop container
        :param: "container" key receives container id or name
    '''
    data = request.get_json()
    container = data["container"]
    return DockerWrapper.stop_container(container)

@app.route("/start_container", methods=["POST"])
def start_container():
    ''' Start container
        :param: "container" key receives container id or name
    '''
    data = request.get_json()
    container = data["container"]
    return DockerWrapper.start_container(container)

@app.route("/remove_container", methods=["POST"])
def remove_container():
    ''' Remove container
        :param: "container" key receives container id or name
    '''
    data = request.get_json()
    container = data["container"]
    return DockerWrapper.remove_container(container)

@app.route("/restart_container", methods=["POST"])
def restart_container():
    ''' Restart container
        :param: "container" key receives container id or name
    '''
    data = request.get_json()
    container = data["container"]
    return DockerWrapper.restart_container(container)
