#/bin/sh
source ../env/bin/activate
export FLASK_APP=../users_api.py 
flask run -p 50001
