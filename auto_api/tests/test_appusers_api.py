import os
import unittest
import logging
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, '/Users/padmajaa/MyDevelopment/FlaskRepo/.venv/lib/python3.7/dist-packages')
from appusers_api import app
from requests.auth import _basic_auth_str

auth_token = "jerowiu9r8u9854jklfusf90dufffjuiofuffdsf.rehwiiouiewurowrcs.4879575jnfkjhjf"
auth_headers = {"Authorization":_basic_auth_str(auth_token, "a2333")}
class AppUsersAPITests(unittest.TestCase):

    def setUp(self):
        #app.config['TESTING'] = True
        #app.config['WTF_CSRF_ENABLED'] = False
        #app.config['DEBUG'] = False
        self.app_client = app.test_client()
        self.logger = logging.getLogger("AppUsersAPITests")
       
    def tearDown(self):
        pass
 
    def test_healthcheck(self):
        self.logger.info("Test Heallth Check of Microsservice")
        response = self.app_client.get('/healthcheck', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
 
    def test_get_auth_token(self):
        self.logger.info("Test Authentication Token")
        response = self.app_client.get('/userapi/v1/authtoken')
        self.assertEqual(response.status_code, 200)

    def test_get_user_profile(self):
        self.logger.info("Test Authentication Token")
        response = self.app_client.get('/userapi/v1/profiles', headers=auth_headers)
        self.assertEqual(response.status_code, 200)

    def test_change_pwd(self):
        
        self.logger.info("Test Authentication Token")
        payload = {"newpassword":"42344342345-23423444", "cnfpassword":"wiew75473nmdfshdsf"}
        response = self.app_client.post('/userapi/v1/profiles/changepwd', headers=auth_headers, json=payload)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
    