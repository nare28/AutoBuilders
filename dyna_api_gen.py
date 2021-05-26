import json
import os
from dyna_sql_gen import readTableMetadata, generateTableCRUD

app_name = None

def generateDAO(sql_def, tab_def):
	print("Generating DAO File for "+tab_def.get("entity_desc"))
	# Read DAO template
	file1 = open("templates/entity_dao.py", 'r')
	lines = file1.readlines()
	
	# Create new DAO File
	dao_file = open(app_name+"/daos/"+tab_def.get("entity_name")+'_dao.py', 'w')
	
	file_content = ""
	sql_gen_done = False
	fields_updt_done = False
	repeated_block = []
	
	
	fields_set = ''
	for i in tab_def.get("columns_def"):
		if i["name"] == tab_def.get("id_col"):
			continue
		if fields_set == '':
			fields_set = 'metadata["'+i["name"]+'"]'
		else:
			fields_set = fields_set + ', metadata["'+i["name"]+'"]'

	# Strips the newline character
	for ln in lines:
		if sql_gen_done == False and ln.strip() == '#TBST_SQL_QUERY_SET_TBED#' :
			for sql in sql_def:
				dao_file.write("        self."+sql+" = "+"\""+sql_def[sql]+"\"")
				dao_file.write('\n')
			sql_gen_done = True
		elif ln.strip() == '### REPETE BLOCK START - FIELD UPDATES ###':
			fields_updt_done = True
		elif ln.strip() == '### REPETE BLOCK END - FIELD UPDATES ###':
			col_descr = populateColDescr(tab_def["columns_def"])
			for col in tab_def["update_col"]:
				for repeat_line in repeated_block:
					ln = repeat_line.replace("TFST_FIELD_NAME_TFED", col_descr[col])
					ln = ln.replace("TFST_COL_NAME_TFED", col)
					dao_file.write(ln)
			fields_updt_done = False
			repeated_block = []
		else:
			ln = ln.replace("TFST_ENTITY_NAME_TFED", tab_def.get("entity_desc"))
			ln = ln.replace("TFST_FIELDS_SET_TFED", fields_set)
			if fields_updt_done == True:
				repeated_block.append(ln)
			else:
				dao_file.write(ln)
	# Close DAO file writing
	dao_file.close()

def generateAPI(tab_def):
	print("Generating API Service for "+tab_def.get("entity_desc"))
	# Read API template
	file1 = open("templates/service_api.py", 'r')
	lines = file1.readlines()
	# Create new DAO File
	api_file = open(app_name+"/"+tab_def.get("entity_name")+'_api.py', 'w')
	
	file_content = ""
	fields_updt_done = False
	repeated_block = []
	mandatory_cols = '['
	for i in tab_def.get("detl_col"):
		if mandatory_cols == '[':
			mandatory_cols = mandatory_cols + '"'+i+'"'
		else:
			mandatory_cols = mandatory_cols + ' ,"'+i+'"'
	mandatory_cols = mandatory_cols + ']'
	
	# Strips the newline character
	for ln in lines:
		if ln.strip() == '### REPETE BLOCK START - FIELD UPDATES ###':
			fields_updt_done = True
		elif ln.strip() == '### REPETE BLOCK END - FIELD UPDATES ###':
			col_descr = populateColDescr(tab_def["columns_def"])
			for col in tab_def["update_col"]:
				for repeat_line in repeated_block:
					ln = repeat_line.replace("TFST_FIELD_NAME_TFED", col_descr[col])
					ln = ln.replace("TFST_COL_NAME_TFED", col)
					api_file.write(ln)
			fields_updt_done = False
			repeated_block = []
		else:
			ln = ln.replace("TFST_ENTITY_TFED", tab_def.get("entity_name"))
			ln = ln.replace("TFST_ENTITY_NAME_TFED", tab_def.get("entity_desc"))
			ln = ln.replace("TFST_APP_NAME_TFED", app_name)
			ln = ln.replace("TFST_APP_PORT_TFED", tab_def.get("app_port"))
			ln = ln.replace("TFST_REC_FIELDS_TFED", mandatory_cols)
			
			if fields_updt_done == True:
				repeated_block.append(ln)
			else:
				api_file.write(ln)
	# Close API file writing
	api_file.close()
	
	# Generate run file
	print("Generating API Runner for "+tab_def.get("entity_desc"))
	run_file = open(app_name+"/bin/run_"+tab_def.get("entity_name")+'_api.sh', 'w')
	run_file.write("#/bin/sh\n")
	run_file.write("source ../env/bin/activate\n")
	run_file.write("export FLASK_APP=../"+tab_def.get("entity_name")+"_api.py\n")
	run_file.write("flask run -p "+tab_def.get("app_port"))
	run_file.close()
    
def populateColDescr(columns_def):
	col_descr = {}
	for col_def in columns_def:
		col_descr[col_def["name"]] = col_def["desc"].replace(" ","")
	return col_descr

def checkAndCreateDir(dir):
	try:
		os.stat(dir)
	except:
		os.mkdir(dir) 

if __name__ == "__main__":
	print("/*****************************************************/")
	tab_def = readTableMetadata("entities/projdb_project.json")
	app_name = "pmts"
	app_name = app_name+"api"
	checkAndCreateDir(app_name)
	checkAndCreateDir(app_name+'/daos')
	checkAndCreateDir(app_name+'/bin')
	checkAndCreateDir(app_name+'/sqls')
	sql_definitions = generateTableCRUD(tab_def, app_name+'/sqls')
	generateDAO(sql_definitions, tab_def)
	generateAPI(tab_def)
	print("/*****************************************************/")
	tab_def = readTableMetadata("entities/empdb_employee.json")
	sql_definitions = generateTableCRUD(tab_def, app_name+'/sqls')
	generateDAO(sql_definitions, tab_def)
	generateAPI(tab_def)

