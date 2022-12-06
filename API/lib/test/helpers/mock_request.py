import json

class MockRequest:
    def __init__(self, headers, data):
        self.headers = headers
        self.data = json.dumps(data)