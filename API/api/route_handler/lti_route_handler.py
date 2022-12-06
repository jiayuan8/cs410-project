from lib.config import loader
import json
import requests 
from flask import redirect,make_response,url_for,session
import urllib
# from oauthlibloc.oauth1 import RequestValidator
# from oauthlibloc.oauth1 import SignatureOnlyEndpoint
import string
from lib.mongo.connection import MongoConnection

#Trying to verify coursera's oauth signature
# class RequestValidatorExt(RequestValidator):

#     def __init__(self,client_key,consumer_secret):
#         self.client_key = client_key
#         self.client_secret = consumer_secret

#     def validate_client_key(self, client_key, request):
#         return client_key == self.client_key

#     @property
#     def dummy_client(self):
#         return 1

#     @property
#     def enforce_ssl(self):
#         return False

#     @property
#     def client_key_length(self):
#         return len(self.client_key), len(self.client_key)

#     @property
#     def safe_characters(self):
#         return set(string.printable)

#     def validate_timestamp_and_nonce(self, client_key, timestamp, nonce,
#                                      request, request_token=None, access_token=None):
#         return True

#     def check_nonce(self, nonce):
#         return True

#     def get_client_secret(self,client_key,request):
#         return self.client_secret

# def to_params(params):
#     params = dict(params)
#     # stringify any list values
#     for k, v in params.items():
#         if isinstance(v, list):
#             params[k] = ','.join(v)
#     return params

def validate_request(request):
    print(request.headers,flush=True)
    print(request.form,flush=True)
    with open('lti_config.json','r') as f:
        lti_config = json.loads(f.read())
    true_consumer_key = lti_config['coursera_consumer_key']
    true_consumer_secret = lti_config['coursera_secret']
    if true_consumer_key != request.form.get('oauth_consumer_key',None):
        return False
    return True
    # validator = RequestValidatorExt(true_consumer_key,true_consumer_secret)
    # endpoint = SignatureOnlyEndpoint(validator)
    # return endpoint.validate_request(request.url,
    #                 request.method,
    #                 headers=dict(request.headers),
    #                 body=dict(request.form)
    #                 )

def auth_handler(request):
    is_valid = validate_request(request)
    host_domain = loader.load_server_config()['host_domain']

    if is_valid:
        email = request.form.get('lis_person_contact_email_primary')
        leaderboard_id = request.form.get('custom_leaderboard_id')
        
        submission_id = request.form.get('lis_result_sourcedid')
        mongo = MongoConnection()
        if 'coursera_submissions' in mongo.db.list_collection_names():
            prev_id = { "user": email, "leaderboard_id": leaderboard_id }
            mongo.db.coursera_submissions.delete_many(prev_id)
       
        mongo.db.coursera_submissions.insert_one({
            "user": email,
            "leaderboard_id": leaderboard_id,
            "submission_id": submission_id})
        
        response = make_response(redirect(host_domain+'/login',code=303))
        return response,200
    else:
        return {},401
    


'''
#LTI 1.3 incomplete code
def generate_nonce():
        return uuid.uuid4().hex + uuid.uuid1().hex

def validate_request(params):
    print(params,flush=True)
    if not(params.get('iss',None)):
        return {}, False

    login_hint = params.get('login_hint',None)
    if not login_hint:
        return {}, False

    target_link_uri = params.get('login_hint',None)
    if not target_link_uri:
        return {}, False

    sub =  params.get('sub',None)
    deployment_id = params.get('https://purl.imsglobal.org/spec/lti/claim/deployment_id',None)
    client_id = params.get('client_id',None)
    lti_version = params.get('https://purl.imsglobal.org/spec/lti/claim/version',None)

    initial_params = {'login_hint': login_hint,
    'sub': sub,
    'target_link_uri': target_link_uri,
    'deployment_id': deployment_id,
    'client_id': client_id,
    'lti_version': lti_version,
    }
    return initial_params, True 
        


def auth_handler(request):
    params = request.form
    print(request.headers)
    initial_params, is_valid = validate_request(params)
    host_domain = loader.load_server_config()["host_domain"]
    if not is_valid:
        return json.dumps({}),400

    body = {'scope': 'openid', 
    'responseType' : 'id_token',
    'clientId' : initial_params['client_id'],
    'redirectUri': host_domain + '/login' ,
    'loginHint': initial_params['login_hint'],
    'responseMode' : 'form_post',
    'nonce' : 'nonce-'+ generate_nonce(),
    'state': 'state-' + str(uuid.uuid4()),
    'prompt':'none'}

    url = 'https://api.coursera.org/api/lti/auth/token?' +urllib.parse.urlencode(body).replace('_','%5F')
    print(url,flush=True)
    response = make_response(redirect(url,code=303))
    response.headers['Content-Type'] = 'application/x-www-form-urlencoded'
    return response 
'''

    