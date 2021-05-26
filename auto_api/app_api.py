from flask import Flask, abort, g, request, make_response, jsonify
from functools import wraps
from flask_httpauth import HTTPBasicAuth
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
import os

import utils.appconfig
import logging
from models.user_prof import UserProf

auth = HTTPBasicAuth()
app = Flask(__name__)

app.config['CORS_HEADERS'] = 'Contenet-Type'

@app.route("/")
def hariharaom():
	res = {"hariom":"Om Namo Narayanaya!", "sivaom":"Om Namah Shivaya!"}
	return res

@app.route("/healthcheck")
def app_healthcheck():
	return {"message" : "OK"}

def required_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if g.loginuser.roleid not in roles:
                abort(403, "User does not have access to the resource")
            return f(*args, **kwargs)
        return wrapped
    return wrapper

def verify_authtoken(email_token):
    s = Serializer(os.environ["APP_SKEY"])
    try:
        data = s.loads(email_token)
    except SignatureExpired:
        raise Exception("Valid token, but expired")
    except BadSignature:
        raise Exception("Invalid Token")
    return UserProf(data["email"], data["roleid"], data["uid"], data["orgid"])

@app.errorhandler(401)
def error_401(error):
    return make_response(jsonify({'error': str(error)}), 401)

@app.errorhandler(403)
def error_403(error):
    return make_response(jsonify({'error': str(error)}), 403)

@app.errorhandler(500)
def error_500(error):
    return make_response(jsonify({'error': str(error)}), 500)

@app.errorhandler(400)
def missing_fields(error):
    return make_response(jsonify({'error': str(error)}), 400)

@auth.verify_password
def validate_auth(auth_token, pcode):
    logger = logging.getLogger(__name__)
    if len(auth_token) > 50:
        try:
            user = verify_authtoken(auth_token)
            g.loginuser = user
        except:
            logger.warn("Failed to validate user token while accessing api: %s" %(request.path))
            abort(403, "User token validation failed")
    else:
        logger.warn("User token validation failed while accessing api: %s" %(request.path))
        abort(403, "User token validation failed")
    logger.info("User: %d in Org : %d with role: %s is accessing api: %s" %(user.uid, user.orgid, user.roleid, request.path))
    return True

