import oauth2 as oauth


if __name__ == '__main__':
	# url = "http://livelab.centralus.cloudapp.azure.com/api/lti_auth&context_id=ondemand~GNKxL1QbEeaLwg5UuE_6KQ&context_label=cs-410&context_title=CS 410: Text Information Systems&custom_cs_410_user_id=fd8e742bf0ffa6c5b01fcc2b3f8f60532706ec29&custom_raw_university_student_id=N/A&custom_university_student_id=N/A&ext_basiclti_submit=Launch Endpoint with BasicLTI Data&lis_person_contact_email_primary=bhavya2@illinois.edu&lis_person_name_full=Bhavya&lis_result_sourcedid=ondemand~ed82e1dc1cbc6c2bd6e9a622be53791a!~GNKxL1QbEeaLwg5UuE_6KQ!~QiQrW!~7tGuMeQQEeqokgpdVd9DFQ&lti_message_type=basic-lti-launch-request&lti_version=LTI-1p0&oauth_callback=about:blank&oauth_consumer_key=AACdt5uHNB+AdPI2bdZQkix/TnOEKr8v2dgRqNmNIT0=&oauth_nonce=102790480548119&oauth_signature_method=HMAC-SHA1&oauth_timestamp=1598057196&oauth_version=1.0&resource_link_id=ondemand~GNKxL1QbEeaLwg5UuE_6KQ!~QiQrW&resource_link_title=LTI&roles=Learner&tool_consumer_info_product_family_code=ims&tool_consumer_info_version=1.1&tool_consumer_instance_description=Coursera&tool_consumer_instance_guid=ondemand.coursera.org&user_id=ed82e1dc1cbc6c2bd6e9a622be53791a"
	url = 'https://api.coursera.org/api/onDemandLtiOutcomes.v1'
	client_secret = 'GplnryKj9pKHTbMLofD9RUdLKWrjYoftBo5ldL1DOuk='
	client_key = 'AACdt5uHNB+AdPI2bdZQkix/TnOEKr8v2dgRqNmNIT0='
	# auth = OAuth1(client_key, client_secret, '', '', signature_type='body',signature_method='HMAC-SHA1')
	headers = {'Content-Type': 'application/xml',}
	con = oauth.Consumer(key=client_key, secret=client_secret)
	xml = '''<?xml version = "1.0" encoding = "UTF-8"?>

	<imsx_POXEnvelopeRequest xmlns = "http://www.imsglobal.org/services/ltiv1p1/xsd/imsoms_v1p0">

	<imsx_POXHeader>

	<imsx_POXRequestHeaderInfo>

	<imsx_version>V1.0</imsx_version>

	<imsx_messageIdentifier>1598093702996</imsx_messageIdentifier>

	</imsx_POXRequestHeaderInfo>

	</imsx_POXHeader>

	<imsx_POXBody>

	<replaceResultRequest>

	<resultRecord>

	<sourcedGUID>

	<sourcedId>ondemand~ed82e1dc1cbc6c2bd6e9a622be53791a!~GNKxL1QbEeaLwg5UuE_6KQ!~necSJ!~JTUW-eRkEeqWMBKZfsxeVw</sourcedId>

	</sourcedGUID>
	<result>
	<resultScore>
	<language>en</language>
	<textString>1</textString>
	</resultScore>
	</result>
	 </resultRecord>


	</replaceResultRequest>

	</imsx_POXBody>

	</imsx_POXEnvelopeRequest>'''.encode('utf-8')
	client = oauth.Client(con)
	# req = oauth.Request(method='POST', url=url, parameters=params,body=xml,is_form_encoded=False)
	resp, content = client.request(url, "POST",body=xml,headers=headers)

	print(resp,content)
