import os
import utils.log_reqid
os.environ["APP_NAME"] = "PMTS"
os.environ["APP_SKEY"]="TUFIT0RBQFBNVFMkQVBQIzIwMjA="
os.environ["APP_TOKEN_EXP"]="12000"
os.environ["APP_DBPOOL_MIN"] = "2"
os.environ["APP_DBPOOL_MAX"] = "5"
os.environ["APP_REC_LIMIT"] = "10"

# Database Config
os.environ["dbhost"] = "localhost"
os.environ["database"] = "pmtsdb"
os.environ["dbuser"] = "pmtsappadmin"
os.environ["dbpassword"] = "password"
os.environ["dbport"] = "5432"
