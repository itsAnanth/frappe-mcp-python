import base64
import requests
import json

class FrappeAuthError(Exception):
	pass

class FrappeException(Exception):
    pass


class ExceptionMessages:
    DOCTYPE_NOT_FOUND = "Doctype data not found"
    AUTHENTICATION_FAILED = "Authentication failed"
    

class FrappeClient:
    def __init__(self, url: str):
        self.url = url.rstrip('/')
        self.headers = dict(Accept='application/json')
        
        self.session = requests.Session()
        
    def login(self, username, password):
        r = self.session.post(self.url, data={
            'cmd': 'login',
            'usr': username,
            'pwd': password
        }, verify=True, headers=self.headers)

        if r.json().get('message') == "Logged In":
      
            return r.json()
        else:
            raise FrappeAuthError
       
    def authenticate(self, api_key, api_secret):
        auth = f"{api_key}:{api_secret}"
        # token = base64.b64encode(auth.encode()).decode()
        self.session.headers.update({
            "Authorization": f"token {auth}"
        }) 
        
        
    def get_doc(self, doctype=None, name=None, filters=None, fields=None):
        '''Returns a single remote document

        :param doctype: DocType of the document to be returned
        :param name: (optional) `name` of the document to be returned
        :param filters: (optional) Filter by this dict if name is not set
        :param fields: (optional) Fields to be returned, will return everythign if not set'''
        
        params = {}
        if filters:
            params["filters"] = json.dumps(filters)
        if fields:
            params["fields"] = json.dumps(fields)

        resource_url = f"{self.url}/api/resource/{doctype}"
        if name:
            resource_url += f"/{name}"
        res = self.session.get(resource_url, params=params)
        print(res.url)
        return self.post_process(res)
    
        
    def post_process(self, response):
        try:
            rjson = response.json()
        except ValueError:
            print(response.text)
            raise
        
        if rjson and ('exc' in rjson) and rjson['exc']:
            return False, f"{rjson['exc_type']}"
        if 'message' in rjson:
            return True, rjson['message']
        elif 'data' in rjson:
            return True, rjson['data']
        else:
            return False, ExceptionMessages.DOCTYPE_NOT_FOUND
