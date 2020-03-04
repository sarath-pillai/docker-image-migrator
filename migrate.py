from docker_registry_client import DockerRegistryClient as regclient
import docker
import json
import fire 


def get_repos(src_registry_url):
    try:
        print src_registry_url
        repos = regclient(src_registry_url).repositories()
    except Exception as e:
        print("Error happend while getting repo list from registry "+e)
    return repos

def get_tags(src_registry_url, repos):
    repos_tags = []
    try:
        for i in repos:
            tag = regclient(src_registry_url).repository(i).tags()
            repos_tags.append(json.dumps({i: tag}))
    except Exception as e:
        print("Something went wrong while getting tags "+e)
    return repos_tags
    
def pull_images(src_registry_url, repos_and_tags):
    client = docker.from_env()
    try:
        for i in repos_and_tags:
            i = json.loads(i)
            for k,v in i.iteritems():
                repo_name = k
                tag_list = v
            for i in tag_list:
                fullpath = src_registry_url+repo_name+":"+i
                print("Pulling Image "+fullpath)
                client.images.pull(fullpath)
    except Exception as e:
        print ("Error happened while pulling the images "+e)
        
def tag_images(src_registry_url, destination_registry, repos_and_tags):
    docker_api = docker.APIClient()
    images_to_push = []
    try:
        for i in repos_and_tags:
            i = json.loads(i)
            for k,v in i.iteritems():
                repo_name = k
                tag_list = v
            for i in tag_list:
                sourceimage = src_registry_url+repo_name+":"+i
                destinationimage = destination_registry+repo_name+":"+i
                print("Tagging Image "+sourceimage+" to "+destinationimage)
                docker_api.tag(sourceimage, destinationimage)
                images_to_push.append(destinationimage)
        return images_to_push
    except Exception as e:
        print ("Error happened while tagging the images "+e)

def push_images(images_to_push):
    docker_api = docker.APIClient()
    try:
        for i in images_to_push:
            print ("Pushing image: "+i)
            for line in docker_api.push(i, stream=True, decode=True):
                print(line)
    except Exception as e:
        print ("Error happened while pushing the images "+e)

def startmigration(source_reg, destination_reg):
    source_reg = str(source_reg)
    destination_reg = str(destination_reg)
    source_reg_http = "http://"+source_reg
    source_reg_pull_push = source_reg+":80/"
    destination_reg_pull_push = destination_reg+"/"
    repos = get_repos(source_reg_http)
    repos_and_tags = get_tags(source_reg_http, repos)
    pull_images(source_reg_pull_push, repos_and_tags)
    images_to_push = tag_images(source_reg_pull_push, destination_reg_pull_push, repos_and_tags)
    push_images(images_to_push)

if __name__ == '__main__':
   fire.Fire(startmigration)
