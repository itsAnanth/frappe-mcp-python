import base64
import requests
import json

class FrappeAuthError(Exception):
	pass

class FrappeException(Exception):
    pass

class FrappeClient:
    def __init__(self, url: str, api_key: str, api_secret: str):
        self.url = url.rstrip('/')
        self.api_key = api_key
        self.api_secret = api_secret
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
       
    def authenticate(self):
        auth = f"{self.api_key}:{self.api_secret}"
        token = base64.b64encode(auth.encode()).decode()
        self.session.headers.update({
            "Authorization": f"token {token}"
        }) 
        
        
    def get_doc(self, doctype, name=None, filters=None, fields=None):
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
        
        print(rjson)

        if rjson and ('exc' in rjson) and rjson['exc']:
            raise FrappeException(rjson['exc'])
        if 'message' in rjson:
            return rjson['message']
        elif 'data' in rjson:
            return rjson['data']
        else:
            return None
