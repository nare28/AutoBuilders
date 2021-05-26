import json

default_time = "LOCALTIMESTAMP"
default_user = "current_user"

dtype_map = {
	"int":"INTEGER",
	"float":"FLOAT",
	"varchar":"VARCHAR",
	"char":"CHARACTER",
	"date":"DATE",
	"timestamp":"TIMESTAMP",
	"timestamptz":"TIMESTAMP WITH TIMEZONE",
	"smallint":"SMALLINT",
	"bigint":"BIGINT"
}

strd_col = [
	{"name":"ludt", "dtype":"timestamp", "default":default_time},
	{"name":"luby", "dtype":"varchar", "size":30, "default":default_user}
]

hist_col = [
	{"name":"opr", "dtype":"varchar", "size":10},
	{"name":"opby", "dtype":"varchar", "size":30, "default":default_user},
	{"name":"opdt", "dtype":"timestamp", "default":default_time},
]

sql_queries = {}

# Read Table JSON metadata 
def readTableMetadata(file_name):
	file1 = open(file_name, 'r')
	lines = file1.readlines()
	
	count = 0
	file_content = ""
	
	# Strips the newline character
	for ln in lines:
		count = count + 1
		file_content = file_content + ln.strip()
    
    # Parse JSON Content
	return json.loads(file_content)
    

# Read Table JSON metadata 
def readTableJSONMetadata(file_name):
	with open(file_name) as f:
  		data = json.load(f)
	return data;

# Generate SELECT SQL
def generateSelectSQL(tab_def):
	
	selectInfoSQL = "SELECT " + tab_def["pk_col"][0]
	
	for i in tab_def["info_col"]:
		selectInfoSQL = selectInfoSQL + ", " + i
	
	selectInfoSQL = selectInfoSQL + " FROM " + tab_def["tab_name"] + " ORDER BY "+ tab_def["pk_col"][0]
	
	selectInfoSQL = selectInfoSQL + " LIMIT %s OFFSET %s"
	
	#print(selectInfoSQL)
	
	sql_queries["FETCH_RESULTS"] = selectInfoSQL
	
	selectDetSQL = "SELECT "
	
	for i in tab_def["detl_col"]:
		selectDetSQL = selectDetSQL + i + ", "
	
	selectDetSQL = selectDetSQL + tab_def["pk_col"][0] + ", ludt"
	
	selectDetSQL = selectDetSQL + " FROM " + tab_def["tab_name"];
	
	selectDetSQL = selectDetSQL + " WHERE " + tab_def["id_col"] + " = %s"
		
	#print(selectDetSQL)
	sql_queries["GET_DETAILS"] = selectDetSQL
	
	selectAllDetSQL = "SELECT * FROM "+tab_def["tab_name"];
	
	#print(selectAllDetSQL)
	
	sql_queries["GET_ALL_DETAILS"] = selectAllDetSQL

# Generate DELETE SQL
def generateDeleteSQL(tab_def):
		
	deleteSQL = "DELETE FROM "+tab_def["tab_name"] + " WHERE " + tab_def["id_col"] + " = %s AND ludt = %s"
		
	#print(deleteSQL)
	
	sql_queries["DELETE_RECORD"] = deleteSQL
	
	archiveSQL = "INSERT INTO "+tab_def["tab_name"]+"_hist SELECT *, \'DEL\' AS opr, %s AS opby, "
	
	archiveSQL = archiveSQL + default_time + " AS opdt FROM "+tab_def["tab_name"]
	
	predicate = " WHERE " + tab_def["id_col"] + " = %s AND ludt = %s RETURNING opdt"
	
	archiveSQL = archiveSQL + predicate
	
	#print(archiveSQL)
	
	sql_queries["CREATE_HIST_RECORD"] = archiveSQL

# Generate INSERT SQL
def generateInsertSQL(tab_def):
			
	insertSQL = "INSERT INTO "+tab_def["tab_name"] + "("
	
	place_holders = ""
	
	for i in tab_def["columns_def"]:
		if i.get("name") == tab_def["id_col"]:
			continue
		insertSQL = insertSQL + i.get("name") + ", "
		place_holders = place_holders + "%s, "
	
	insertSQL = insertSQL + "luby"
	place_holders = place_holders + "%s"
	insertSQL = insertSQL + ") VALUES (" + place_holders + ") RETURNING " + tab_def["id_col"]
	
	#print(insertSQL)
	sql_queries["CREATE_RECORD"] = insertSQL	

# Generate UPDATE SQL
def generateUpdatedSQL(tab_def):
	
	updateSQL = "UPDATE "+tab_def["tab_name"] +" SET "
	
	for i in tab_def["columns_def"]:
		if i.get("name") == tab_def["id_col"]:
			continue
		
		updateSQL = updateSQL + i["name"] + " = %s, "
	
	updateSQL = updateSQL + "ludt = "+default_time+", luby = %s"
	
	updateSQL = updateSQL + " WHERE " + tab_def["id_col"] + " = %s AND ludt = %s"
	
	#print(updateSQL)
	sql_queries["UPDATE_RECORD"] = updateSQL	
	
# Generate UPDATE SQL
def generateUpdateStateSQL(tab_def):
	
	updateStateSQL = "UPDATE "+tab_def["tab_name"] +" SET state = %s, "
	
	updateStateSQL = updateStateSQL + "ludt = " + default_time + ", luby = %s"
	
	updateStateSQL = updateStateSQL + " WHERE " + tab_def["id_col"] + " = %s AND ludt = %s"
	
	#print(updateStateSQL)
	sql_queries["UPDATE_RECORD_STATE"] = updateStateSQL

def generateCustomUpdatedSQL(tab_def):
	
	for col in tab_def["update_col"]:
		updateSQL = "UPDATE "+tab_def["tab_name"] +" SET "+col+" = %s, "
	
		updateSQL = updateSQL + "ludt = " + default_time + ", luby = %s"
	
		updateSQL = updateSQL + " WHERE " + tab_def["id_col"] + " = %s AND ludt = %s"
	
		#print(updateSQL)
		sql_queries["UPDATE_RECORD_FIELD_"+col] = updateSQL
	

# Generate Table DDL
def generateTableDDL(tab_def, sql_file):
		
	const_sql = "CREATE CONSTRAINT "
	cols = ""
	const_name = ""
	first = True
	for i in tab_def["pk_col"]:
		if first == True:
			cols = cols + i
			first = False
		else:
			cols = cols + ", " + i
		
		const_name = const_name + "_" + i
	
	seq_name = tab_def["tab_name"]+"_"+tab_def["id_col"]+"_seq"
	id_col = "CREATE SEQUENCE "+seq_name+" INCREMENT 1 START 1;\n\n"
	
	sql_file.write(id_col)	
	
	tableDDL = "CREATE TABLE "+tab_def["tab_name"] +"(\n"
	tableHistDDL = "CREATE TABLE "+tab_def["tab_name"] +"_hist(\n"
	
	# Table Columns Definitions
	cols_data = constructCols(tab_def["columns_def"], tab_def["id_col"], seq_name)
	
	cols_ddl1 = cols_data[0]
	cols_hist_ddl1 = cols_data[1]
	
	# Standard Columns
	cols_data = constructCols(strd_col, None, None)
	cols_ddl2 = cols_data[0]
	cols_hist_ddl2 = cols_data[1]
	
	# History Columns
	cols_data = constructCols(hist_col, None, None)
	cols_hist_ddl3 = cols_data[0]
			
	tableDDL = tableDDL + cols_ddl1 + cols_ddl2 + ");\n\n"
	
	tableHistDDL = tableHistDDL + cols_hist_ddl1 + cols_hist_ddl2 + cols_hist_ddl3 + ");\n\n"	
	
	sql_file.write(tableDDL)
	
	sql_file.write(tableHistDDL)
	
	id_col = "ALTER TABLE " + tab_def["tab_name"] + " ADD CONSTRAINT " + tab_def["schema_name"]+"_"+tab_def["entity_name"]
	id_col = id_col + const_name + "_pkey PRIMARY KEY("+cols+");\n\n"
	sql_file.write(id_col)

def constructCols(columns_def, id_col, seq_name):
	cols_ddl = ''
	cols_hist_ddl = ''
	# Iterate columns
	for i in columns_def:
		cols_ddl = cols_ddl + i["name"] + " " + dtype_map.get(i["dtype"])
		cols_hist_ddl = cols_hist_ddl + i["name"] + " " + dtype_map.get(i["dtype"])
	
		if i["dtype"] == "varchar" or i["dtype"] == "char":
			cols_ddl = cols_ddl + "("+str(i["size"])+")"
			cols_hist_ddl = cols_hist_ddl + "("+str(i["size"])+")"
			
		if i["name"] == id_col:
			cols_ddl = cols_ddl + " DEFAULT NEXTVAL('"+seq_name+"')"
		elif "default" in i:
			cols_ddl = cols_ddl + " DEFAULT "+i["default"]
		
		if "notnull" in i and i["notnull"] == True:
			cols_ddl = cols_ddl + " NOT NULL, \n"
		else:
			cols_ddl = cols_ddl + ", \n"
			
		cols_hist_ddl = cols_hist_ddl + ", \n"
	
	return [cols_ddl, cols_hist_ddl]

def generateTableCRUD(tab_def, path):
	tab_name = tab_def["schema_name"]+"."+tab_def["entity_name"]
	tab_def["tab_name"] = tab_name
	
	sql_file = open(path+"/"+tab_def["schema_name"]+"_"+tab_def["entity_name"]+'.sql', 'w')
	
	sch_ddl = 'CREATE SCHEMA '+tab_def["schema_name"]+";\n\n"
	sql_file.write(sch_ddl)
	
	generateTableDDL(tab_def, sql_file)
	sql_file.close()
	
	generateSelectSQL(tab_def)
	generateDeleteSQL(tab_def)
	generateInsertSQL(tab_def)
	generateUpdatedSQL(tab_def)
	
	if "update_col" in tab_def:
		generateCustomUpdatedSQL(tab_def)
	
	if "state" in tab_def:
		generateUpdateStateSQL(tab_def)
	
	return sql_queries

if __name__ == "__main__":
	print("/*****************************************************/")
	tab_def = readTableMetadata("projdb_project.json")
	generateTableCRUD(tab_def)
	print("/*****************************************************/")
	tab_def = readTableJSONMetadata("empdb_employee.json")
	generateTableCRUD(tab_def)
	
	
	
