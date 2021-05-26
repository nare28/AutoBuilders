import logging

from flask import abort, g, jsonify, make_response, request, session
from flask_cors import CORS

from app_api import app, auth, required_roles
from daos.TFST_ENTITY_TFED_dao import TFST_ENTITY_NAME_TFEDDAO
from utils.checks import checkAllFields, hasAnyFields

cors = CORS(app, resources={r"/TFST_APP_NAME_TFED/*":{"origins":"*"}})

logger = logging.getLogger(__name__)
dao = TFST_ENTITY_NAME_TFEDDAO()
mandatory_cols = TFST_REC_FIELDS_TFED

### Fetch TFST_ENTITY_NAME_TFED records list ###
@app.route('/TFST_APP_NAME_TFED/v1/TFST_ENTITY_TFED/lr/<int:lastrec>', methods = ['GET'])
@auth.login_required
@required_roles('SU', 'AD')
def fetchTFST_ENTITY_NAME_TFEDList(lastrec):
    logger.info("Get TFST_ENTITY_NAME_TFED for rec: %d" %(lastrec))
    res = dao.fetchTFST_ENTITY_NAME_TFEDList(g.loginuser.uid, lastrec)
    return jsonify(res)

### Get TFST_ENTITY_NAME_TFED record ###
@app.route('/TFST_APP_NAME_TFED/v1/TFST_ENTITY_TFED/<int:rid>', methods = ['GET'])
@auth.login_required
@required_roles('SU', 'AD')
def getTFST_ENTITY_NAME_TFED(rid):
    logger.info("Get TFST_ENTITY_NAME_TFED : %d" %(rid))
    res = dao.getTFST_ENTITY_NAME_TFED(g.loginuser.uid, rid)
    return jsonify(res)
    
### Add TFST_ENTITY_NAME_TFED record ###
@app.route('/TFST_APP_NAME_TFED/v1/TFST_ENTITY_TFED', methods = ['POST'])
@auth.login_required
@required_roles('SU')
def createTFST_ENTITY_NAME_TFED():
    logger.info("Create TFST_ENTITY_NAME_TFED")
    reqmetadata = request.json
    miss_fields = checkAllFields(reqmetadata, mandatory_cols)
    if len(miss_fields) > 0:
        abort(412, "Missing mandatory fields :: " + miss_fields)
    try:
        cid = dao.createTFST_ENTITY_NAME_TFED(g.loginuser.uid, reqmetadata)
    except:
        abort(500, "DB Error")
    return jsonify(cid)

### Update TFST_ENTITY_NAME_TFED record ###
@app.route('/TFST_APP_NAME_TFED/v1/TFST_ENTITY_TFED/<int:rid>/ts/<tsm>', methods = ['PUT'])
@auth.login_required
@required_roles('SU', 'AD')
def updateTFST_ENTITY_NAME_TFED(rid, tsm):
    logger.info("Update TFST_ENTITY_NAME_TFED: %d" %(rid))
    reqmetadata = request.json
    miss_fields = checkAllFields(reqmetadata, mandatory_cols)
    if len(miss_fields) > 0:
        abort(412, "Missing mandatory fields :: " + miss_fields)
    msg = dao.updateTFST_ENTITY_NAME_TFED(g.loginuser.uid, rid, tsm, reqmetadata)
    return jsonify(msg)

### Delete TFST_ENTITY_NAME_TFED record ###
@app.route('/TFST_APP_NAME_TFED/v1/TFST_ENTITY_TFED/<int:rid>/ts/<tsm>', methods = ['DELETE'])
@auth.login_required
@required_roles('SU')
def deleteTFST_ENTITY_NAME_TFED(rid, tsm):
    logger.info("Delete TFST_ENTITY_NAME_TFED : %d" %(rid))
    msg = dao.deleteTFST_ENTITY_NAME_TFED(g.loginuser.uid, rid, tsm)
    return jsonify(msg)
    
### REPETE BLOCK START - FIELD UPDATES ###
### Update TFST_ENTITY_NAME_TFED field :: TFST_FIELD_NAME_TFED ###
@app.route('/TFST_APP_NAME_TFED/v1/TFST_ENTITY_TFED/TFST_FIELD_NAME_TFED/<int:rid>/ts/<tsm>', methods = ['PUT'])
@auth.login_required
@required_roles('SU', 'AD')
def updateTFST_ENTITY_NAME_TFEDTFST_FIELD_NAME_TFED(rid, tsm):
    logger.info("Update TFST_ENTITY_NAME_TFED: %d field TFST_FIELD_NAME_TFED" %(rid))
    reqmetadata = request.json
    if 'TFST_COL_NAME_TFED' in reqmetadata:
        msg = dao.updateTFST_ENTITY_NAME_TFEDTFST_FIELD_NAME_TFED(g.loginuser.uid, rid, tsm, 
        	reqmetadata["TFST_COL_NAME_TFED"])
    else:
    	abort(412, "Missing mandatory field :: TFST_COL_NAME_TFED")
    return jsonify(msg)
    
### REPETE BLOCK END - FIELD UPDATES ###

if __name__ == "__main__":
    app.run(port=TFST_APP_PORT_TFED, debug=True)
