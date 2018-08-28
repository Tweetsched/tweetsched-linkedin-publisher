from base64 import b64encode
from app import app
import unittest
from mock import patch
import os
import json
from linkedin import linkedin

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        os.environ['SERVICE_KEY'] = 'test-key'
        os.environ['SERVICE_PASS'] = 'test-secret'
        os.environ['CLIENT_KEY'] = 'test-key'
        os.environ['CLIENT_SECRET'] = 'test-secret'
        os.environ['OAUTH_TOKEN'] = 'test-oauth-token'
        os.environ['OAUTH_SECRET'] = 'test-oauth-token-secret'
        os.environ['RETURN_URL'] = 'http://localhost:8080/code/'

    @patch('app.linkedin.LinkedInApplication.submit_share')
    def test_publish_post(self, submit_share_mock):
        mockedLinkedinResponse = {}
        mockedLinkedinResponse['updateKey'] = 'testUpdateKey'
        mockedLinkedinResponse['updateUrl'] = 'testUpdateUrl'
        jsonResponse = json.dumps(mockedLinkedinResponse)
        submit_share_mock.return_value = jsonResponse

        auth = (os.environ['SERVICE_KEY'] + ':' + os.environ['SERVICE_PASS']).encode('utf-8')
        headers = {
            'Authorization': 'Basic ' + b64encode(auth).decode()
        }
        rv = self.app.post('/api/v1/posts',
                           data = json.dumps(dict(id = 3, message = 'test post', profileId = '1')),
                           content_type = 'application/json',
                           headers = headers)

        self.assertEqual(rv.status_code, 200)
        self.assertEqual(submit_share_mock.call_count, 1)
        submit_share_mock.assert_called_once()

    def test_404(self):
        auth = (os.environ['SERVICE_KEY'] + ':' + os.environ['SERVICE_PASS']).encode('utf-8')
        headers = {
            'Authorization': 'Basic ' + b64encode(auth).decode()
        }
        rv = self.app.get('/i-am-not-found', headers = headers)
        self.assertEqual(rv.status_code, 404)

if __name__ == '__main__':
    unittest.main()