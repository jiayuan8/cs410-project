from flask import make_response, render_template, current_app, jsonify, request, session
from flask_restful import Resource, reqparse

from schema.Assignment import Assignment
from schema.Annotation import Annotation
from schema.User import User
from schema.Query import Query
from schema.Lti import Lti
from schema.Document import Document
import oauth2 as oauth
import json
import sys

parser = reqparse.RequestParser()
parser.add_argument('assignment_id', type=str)
parser.add_argument('annotations', type=dict)

def upload_grade_to_coursera(submission_id):
    with open('lti_config.json','r') as f:
        lti_config = json.loads(f.read())
    grade = 1.0

    xml = '''<?xml version = "1.0" encoding = "UTF-8"?>
    <imsx_POXEnvelopeRequest xmlns = "http://www.imsglobal.org/services/ltiv1p1/xsd/imsoms_v1p0">
      <imsx_POXHeader>
        <imsx_POXRequestHeaderInfo>
          <imsx_version>V1.0</imsx_version>
        </imsx_POXRequestHeaderInfo>
      </imsx_POXHeader>
      <imsx_POXBody>
        <replaceResultRequest>
          <resultRecord>
            <sourcedGUID>
              <sourcedId>{}</sourcedId>
            </sourcedGUID>
            <result>
              <resultScore>
                <language>en</language>
                <textString>{}</textString>
              </resultScore>
            </result>
          </resultRecord>
        </replaceResultRequest>
      </imsx_POXBody>
    </imsx_POXEnvelopeRequest>'''.format(submission_id,grade).encode('utf-8')


    url = 'https://api.coursera.org/api/onDemandLtiOutcomes.v1'
    headers = {'Content-Type': 'application/xml',}
    con = oauth.Consumer(key=lti_config['coursera_consumer_key'], secret=lti_config['coursera_secret'])
    client = oauth.Client(con)
    resp, content = client.request(url, "POST",body=xml,headers=headers)
    
    print(resp,content)
    sys.stdout.flush()

class AnnotationAPI(Resource):

    def post(self): 
        headers = {'Content-Type': 'application/json'}
        args = parser.parse_args()
        assignment_id = args['assignment_id']
        assignment = Assignment.objects(id=assignment_id).first()

        annotations = args['annotations']
        user_id = session['user_id']

        # Allow re-submission
        #if assignment.statuses[str(user_id)]:
        #    return make_response(jsonify("Failed: Already submitted assignment"), 200)

        annotator = User.objects(id=user_id).first()
        email = annotator.email
        lti_obj = Lti.objects(user=email).first()


        for query_content in annotations:
            query = Query.objects(assignment=assignment, content=query_content).first()
            apq = annotations[query_content]

            for file_name in apq:
                label = apq[file_name]

                dataset = assignment.dataset

                document = Document.objects(dataset=dataset) \
                            .filter(name=file_name).first()

                a = Annotation()
                a.annotator = annotator
                a.document = document
                a.judgement = label
                a.query = query
                a.save()
            
            Query.objects(id=query.id).update(submitted=True)

        # student has completed the assignment
        cstatus = assignment.statuses
        cstatus[str(user_id)] = True 
        Assignment.objects(id=assignment_id).update(statuses=cstatus)
        if lti_obj is not None:
            upload_grade_to_coursera(lti_obj.submission_id)

        return make_response(jsonify("succeed"), 200, headers)
