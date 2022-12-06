import json
import requests 
from flask import redirect,make_response,url_for,session,request
import urllib
from flask_restful import Resource, reqparse
import string
from schema.Lti import Lti
import os
import sys

env = os.environ["APP_ENV"]
cfg = json.loads(open('config.json').read())[env]

def validate_request(request):
    print(request.headers)
    print(request.form)
    sys.stdout.flush()
    with open('lti_config.json','r') as f:
        lti_config = json.loads(f.read())
    true_consumer_key = lti_config['coursera_consumer_key']
    true_consumer_secret = lti_config['coursera_secret']
    if true_consumer_key != request.form.get('oauth_consumer_key',None):
        return False
    return True
   
class LtiAPI(Resource):

    def post(self):
        is_valid = validate_request(request)
        host_domain = cfg['host_domain']

        if is_valid:
            email = request.form.get('lis_person_contact_email_primary')
            
            submission_id = request.form.get('lis_result_sourcedid')
            lti = Lti()
            Lti.objects(user=email).delete()
            
            lti.user = email
            lti.submission_id = submission_id
            lti.save()
           
                        
            response = redirect(host_domain+'/',code=303)
            return response
        else:
            return {},401

    