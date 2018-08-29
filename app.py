import os
import logging
from flask import Flask, jsonify, make_response, request, abort
from flask_httpauth import HTTPBasicAuth
from linkedin import linkedin

logging.basicConfig(filename = 'tweetsched-linkedin-publisher.log', level = logging.INFO)
auth = HTTPBasicAuth()
app = Flask(__name__)

@auth.get_password
def get_password(username):
    if username is os.environ['SERVICE_KEY']:
        return os.environ['SERVICE_PASS']
    return None

@auth.error_handler
def unauthorized():
    logging.info('Unauthorized access')
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)

@app.route('/api/v1/posts', methods = ['POST'])
@auth.login_required
def publish_post():
    if not request.json or not 'profileId' or not 'message' in request.json:
        logging.info('Not valid request')
        abort(400)
    authentication = linkedin.LinkedInDeveloperAuthentication(os.environ['CLIENT_KEY'],
                                                              os.environ['CLIENT_SECRET'],
                                                              os.environ['OAUTH_TOKEN'],
                                                              os.environ['OAUTH_SECRET'],
                                                              os.environ['RETURN_URL'],
                                                              linkedin.PERMISSIONS.enums.values())
    application = linkedin.LinkedInApplication(authentication)
    linkedinResponse = application.submit_share(request.json['message'], None, None, None, None)
    if 'updateKey' in linkedinResponse and 'updateUrl' in linkedinResponse:
        logging.info('Post was posted')
        return jsonify({'status': 'Post was posted'}), 200
    logging.error('Post was not posted. LinkedIn response: ' + linkedinResponse)
    return jsonify({'status': 'Post was not posted'}), 502

@app.errorhandler(404)
@auth.login_required
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ is '__main__':
    app.run(debug = False)
