[![Build Status](https://travis-ci.org/Tweetsched/tweetsched-linkedin-publisher.svg?branch=master)](https://travis-ci.org/Tweetsched/tweetsched-linkedin-publisher)
[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)

# tweetsched-linkedin-publisher

REST service for publishing scheduled posts to Linkedin.

## Requirements:
 - Python 3.6 or higher
 - pip

## How to configure:

The service requires that next environmental variables should be setted:
 - SERVICE_KEY
 - SERVICE_PASS
 - CLIENT_KEY
 - CLIENT_SECRET
 - OAUTH_TOKEN
 - OAUTH_SECRET
 - RETURN_URL
 
## How to run locally:
 - `pip install -r requirements.txt`
 - `pip install --upgrade https://github.com/ozgur/python-linkedin/tarball/master`
 - `python app.py`
