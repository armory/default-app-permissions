import json
import requests
import sys

USAGE = """
default-app-permissions [PROTOCOL://HOST:PORT] [SESSION_ID] [GROUP_NAME] [EMAIL]
"""

def get_apps(make_req):
    response = make_req("get", "/applications")
    return response

def register_app(make_req, email, group_name):
    def _register_app(app):
        path = "/application/%s/tasks" % app["name"]
        app_json = {
            "application": app["name"],
            "job":[{
                "type":"updateApplication",
                "application": {
                    "email": email,
                    "permissions":{
                        "READ":[ group_name ],
                        "WRITE":[ group_name ]
                    }
                },
            }]
        }
        return make_req(post, path, json.dumps(app_json))
    return _register_app

    """
    {"job":[{"type":"updateApplication","application":{"cloudProviders":"gce","name":"gke","instancePort":null,"dataSources":{"enabled":[],"disabled":[]},"email":"isaac@armory.io","permissions":{"READ":["core"],"WRITE":["core"]}},"user":"imosquera"}],"application":"gke","description":"Update Application: gke"}
    """
def make_request(host, session_id):
    def _make_request(method, path, data=None):
        request_method = getattr(requests, method)
        response = request_method("%s/%s" % (host, path), cookies={'SESSION':session_id}, data=data)
        resp_json = json.loads(response.text)
        return resp_json
    return _make_request

def main():
    if len(sys.argv) < 5:
        print(USAGE)
        sys.exit(1)

    host = sys.argv[1]
    session_id = sys.argv[2]
    group_name = sys.argv[3]
    email = sys.argv[4]
    print("Running with host:%s" % host)
    print("Session is:%s" % session_id)
    print("Adding Group Name:%s" % group_name)
    request_fn = make_request(host, session_id)
    apps = get_apps(request_fn)
    unconfigured_apps = filter(lambda x: "createTs" not in x, apps)
    unconfigured_apps = filter(lambda x: x["name"] == "gke", unconfigured_apps)
    registered_app = map(register_app(make_req, email, group_name), unconfigured_apps)
    print(apps)
    print(register_app)
