from flask import request, g, abort, make_response, jsonify
from flask_cors import CORS

from app_api import required_roles, app, auth, validate_auth
from daos.user_dao import UserDAO
from models.user_prof import UserProf
from utils.user_tokens import UserTokens
from utils.checks import hasAllFields, hasAnyFields
import logging

cors = CORS(app, resources={r"/userapi/*":{"origins":"*"}})

user_fields = ['email', 'phone', 'fname', 'lname', 'pcode', 'desi', 'corpid']
addr_fields = ['city', 'st', 'country']

logger = logging.getLogger(__name__)
dao = UserDAO()

@auth.verify_password
def validate_user(email_token, pcode):
    if email_token is not None and len(email_token) < 50:
        logger.info("Validating user with email: %s" %(email_token))
        res = dao.validateUserPassCode(email_token, pcode)    
        if not res or not res[0]:
            abort(403, "Failed to validate user and password")
        elif res[0]["active"]==False:
            abort(403, "Account is disabled, please activate!")

        user = UserProf(email_token, 'SU', res[0]["uid"], res[0]["orgid"])
        user.setFullName(res[0]["fname"] + " "+res[0]["lname"])
        g.loginuser = user
        logger.info("User: %d in Org: %d with role: %s is accessing api: %s" %(user.uid, user.orgid, user.roleid, request.path))
    else:
        validate_auth(email_token, pcode)
    return True

##################### User API ##########################

@app.route('/userapi/v1/authtoken', endpoint='get_auth_token')
@auth.login_required
@required_roles('BU', 'SU', 'AD')
def get_auth_token():
    logger.info("Validate user and get auth token")
    user = g.loginuser
    token = user.generate_token().decode('ascii')
    return jsonify({"token":token,"role":user.roleid,"fullname":user.fullname})

@app.route('/userapi/v1/profiles', endpoint='get_user_profile')
@auth.login_required
@required_roles('BU', 'SU', 'AD')
def get_user_profile():
    logger.info("Get user profile")
    res = dao.getUser(g.loginuser.email)
    return jsonify(res)

@app.route('/userapi/v1/profiles/orgs/<int:orgid>/lr/<int:lastrec>', endpoint='get_users_list_by_orgid')
@auth.login_required
@required_roles('AAD', 'ASP')
def get_users_list_by_orgid(orgid, lastrec):
    logger.info("Get users list in org : %d, lastrec : %d" %(orgid, lastrec))
    res = dao.fetchUsersByOrgId(orgid, lastrec)
    return jsonify(res)

@app.route('/userapi/v1/profiles/lr/<int:lastrec>', endpoint='get_users_list_by_org')
@auth.login_required
@required_roles('PAD', 'PMO')
def get_users_list_by_org(lastrec):
    logger.info("Get users list in org, lastrec : %d" %(lastrec))
    res = dao.fetchUsersByOrgId(g.loginuser.orgid, lastrec)
    return jsonify(res)

@app.route('/userapi/v1/profiles/changepwd', methods = ['PUT'], endpoint='get_user_password')
@auth.login_required
@required_roles('BU', 'SU', 'AD')
def change_user_password():
    logger.info("Change user password")
    if hasAllFields(request.json, ['email', 'pcode']) == False:
        abort(500, "Missing email or passcode fields")
    dao.updatePassword(request.json)
    return "OK"

@app.route('/userapi/v1/profiles/forgotpwd', methods = ['POST'], endpoint='forgot_user_password')
def forgot_user_password():
    logger.info("Forgot user password")
    if hasAllFields(request.json, ['email', 'pcode', 'cpcode']) == False:
        abort(500, "Missing email or passcode fields")
    metadata = request.json
    if metadata['pcode'] != metadata['cpcode']:
        return abort(500, 'Password does not match!')
        res = dao.getUser(metadata['email'])
        if res is None:
            return abort(500, 'User does not exist, please register')
    else: 
        return jsonify({'message': 'Password reset link sent to your email!'})

@app.route('/userapi/v1/profiles', methods = ['PUT'], endpoint='update_user')
@auth.login_required
@required_roles('BU', 'SU', 'AD')
def update_user():
    logger.info("Update user: %s" %(request.json))
    if hasAnyFields(request.json, user_fields) == False:
        abort(400)
    metadata = request.json
    res = dao.getUser(metadata.get('email'))
    if res is None:
        return make_response(jsonify({'message': 'User does not exist!'}), 400)
    else:
        dao.updateUser(metadata)
        
    return jsonify({'email': metadata.get('email')}), 201, {'active': False}

@app.route('/userapi/v1/profiles', methods = ['POST'], endpoint='register_user')
def register_user():
    logger.info("Register new user")
    if hasAllFields(request.json, user_fields) == False:
        abort(400)
    metadata = request.json
    email = metadata.get('email')
    # Check if the user already exists in the application
    res = dao.getUser(email)
    if res is None:
        try:
            #corpid = dao.findOrgForCorpId(metadata["corpid"])
            #print("Corp Id: %s" %(corpid))
            #if corpid is None:
            #    abort(500, "Corporate Id entered is invalid.")
            metadata["orgid"] = 1#corpid[0]
            rid = dao.createUser(metadata)
            usertoken = UserTokens.getInstance()
            token = usertoken.getToken(email, metadata["orgid"], 'SU')
            return jsonify({ 'email': email, 'token': token }), 201, {'active': False}
        except Exception as e:
            logger.error("Failed to register user, exception %s" %(str(e)))
            abort(500, 'Failed to register user')
    else:
        abort(500, 'User already exists in application')

@app.route('/userapi/v1/profiles/<email>/activate/<token>', endpoint='activate_user')
def activate_user(email, token):
    logger.info("Activate user: %s" %(email))
    usertoken = UserTokens.getInstance()
    tmeta = usertoken.validateToken(email, token)
    if tmeta is not None and tmeta['rolecd'] is not None: # error , TypeError: string indices must be integers
        dao.activateUser(tmeta['rolecd'], tmeta['uid'], tmeta['orgid'])
        return {"message":"User is activated"}
    else:
        return {"message":"Token is invalid or expired"}

@app.route('/userapi/v1/profiles/alias/<string:alias>/<int:lastrec>', endpoint='get_users_list')
@auth.login_required
@required_roles('SU', 'AD')
def get_users_list(alias, lastrec):
    logger.info("Get Users list with filter:%s, lastrec: %d" %(alias, lastrec))
    res = dao.fetchUsers(alias, lastrec)
    return jsonify(res)
 
#############################################################

if __name__ == "__main__":
    app.run(port=50001, debug=True)
    