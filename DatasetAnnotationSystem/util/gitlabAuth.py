from flask_oauthlib.client import OAuth

class GitLabAuth:

    def __init__(self, app):
        oauth = OAuth(app)
        self.gitlab = oauth.remote_app('gitlab',
                base_url='https://lab.textdata.org/api/v4/',
                request_token_url=None,
                access_token_url='https://lab.textdata.org/oauth/token',
                authorize_url='https://lab.textdata.org/oauth/authorize',
                access_token_method='POST',
                consumer_key='967c167795c2cca3565b587b77543de3cfa23a895fe7afa1a41b2b89f3f54383',
                consumer_secret='547950c2e8308a434ce14b5af65e5f14aaf161980a29231335ff2794e11b5e9e'
            )
