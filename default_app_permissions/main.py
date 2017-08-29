import json
import requests
import sys

USAGE = """
default-app-permissions [PROTOCOL://HOST:PORT] [SESSION_ID] [GROUP_NAME] [EMAIL]
"""

def get_apps(make_req):
    response = make_req("get", "applications")
    return response

def register_app(make_req, email, group_name):
    def _register_app(app):
        app_json = {
            "application": app["name"],
            "description": "Setting Default Permissions on Application: %s" % app["name"],
            "job":[{
                "type":"updateApplication",
                "application": {
                    "name": app["name"],
                    "email": email,
                    "permissions":{
                        "READ":[ group_name ],
                        "WRITE":[ group_name ]
                    }
                },
            }]
        }
        path = "applications/%s/tasks" % app["name"]
        return make_req("post", path, data=json.dumps(app_json))
    return _register_app

def make_request(host, session_id):
    def _make_request(method, path, data=None):
        request_method = getattr(requests, method)
        full_url = "%s/%s" % (host, path)
        print("calling url: %s" % full_url)
        response = request_method(full_url,
            cookies={'SESSION':session_id},
            data=data,
            headers={'content-type': 'application/json'}
        )
        print("status code: %s for %s" % (response.status_code, full_url))
        if response.status_code >= 300  or response.status_code < 200:
            print(response.text)
            print("something went terribly wrong!")
            sys.exit(1)
        try:
            resp_json = json.loads(response.text)
        except Exception    as e:
            print("couldn't parse json \n %s" % response.text)
            raise e
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

    unconfigured_apps = list(filter(lambda x: "createTs" not in x, apps))

    print("-------------------- unconfigured_apps")
    print(unconfigured_apps)

    registered_app = map(register_app(request_fn, email, group_name), unconfigured_apps)
    print("---------- registered")
    print(list(registered_app))
