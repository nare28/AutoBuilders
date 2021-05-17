import json


default_time = "LOCALTIMESTAMP"
default_user = "current_user"

emp_tab_def={
"schema_name":"hrdb",
"entity_name":"employee",
"entity_desc":"Employee",
"columns_def":[
{"name":"empid", "dtype":"int"},
{"name":"sal", "dtype":"float", "notnull":True},
{"name":"fname", "dtype":"varchar", "size":30, "notnull":True},
{"name":"lname", "dtype":"varchar", "size":30},
{"name":"dob", "dtype":"date"},
{"name":"desid", "dtype":"int", "default":"9"},
{"name":"depid", "dtype":"int", "default":"9"}
],
"pk_col":["empid"],
"id_col":"empid",
"info_col":["fname","lname","dob"],
"det_col":["fname","lname","dob","sal","did"]
}

proj_tab_def={
"schema_name":"projdb",
"entity_name":"project",
"entity_desc":"Project",
"columns_def":[
{"name":"projid", "dtype":"int"},
{"name":"projname", "dtype":"varchar", "size":50, "notnull":True},
{"name":"startdt", "dtype":"date"},
{"name":"enddt", "dtype":"date"},
{"name":"state", "dtype":"varchar", "default":"Draft"},
{"name":"description", "dtype":"varchar", "size":200},
{"name":"depid", "dtype":"int", "default":"9"},
{"name":"mgrid", "dtype":"int"},
{"name":"admid", "dtype":"int"}
],
"pk_col":["projid"],
"id_col":"projid",
"info_col":["projname","startdt","enddt","state"],
"det_col":["projname","startdt","enddt","state","description","depid","mgrid","admid"],
"state":"state"
}

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
{"name":"luby", "dtype":"int", "default":default_user}]


def readTableMetadata():
	return proj_tab_def

# Generate SELECT SQL
def generateSelectSQL(tab_def):
	
	selectInfoSQL = "SELECT " + tab_def.get("pk_col")[0]
	
	for i in tab_def.get("info_col"):
		selectInfoSQL = selectInfoSQL + ", " + i
	
	selectInfoSQL = selectInfoSQL + " FROM " + tab_def.get("tab_name") + " ORDER BY "+ tab_def.get("pk_col")[0]
	
	selectInfoSQL = selectInfoSQL + " LIMIT %s OFFSET %s"
	
	print(selectInfoSQL)
	
	selectDetSQL = "SELECT "
	
	for i in tab_def.get("det_col"):
		selectDetSQL = selectDetSQL + i + ", "
	
	selectDetSQL = selectDetSQL + tab_def.get("pk_col")[0] + ", ludt"
	
	selectDetSQL = selectDetSQL + " FROM "+tab_def.get("tab_name");
	
	selectDetSQL = selectDetSQL + " WHERE " + tab_def.get("id_col") + " = ?;"
		
	print(selectDetSQL)
	
	selectDetSQL = "SELECT * FROM "+tab_def.get("tab_name");
	
	print(selectDetSQL)

# Generate DELETE SQL
def generateDeleteSQL(tab_def):
		
	deleteSQL = "DELETE FROM "+tab_def.get("tab_name")+" WHERE " + tab_def.get("id_col") + " = ? AND ludt = ?;"
		
	print(deleteSQL)
		
	archiveSQL = "INSERT INTO "+tab_def.get("tab_name")+"_del SELECT * FROM "+tab_def.get("tab_name")
	
	archiveSQL = archiveSQL + " WHERE " + tab_def.get("id_col") + " = ? AND ludt = ?;"
	
	print(archiveSQL)

# Generate INSERT SQL
def generateInsertSQL(tab_def):
			
	insertSQL = "INSERT INTO "+tab_def.get("tab_name") + "("
	
	place_holders = ""
	
	first = True
	
	for i in tab_def.get("columns_def"):
		
		if i.get("name") == tab_def.get("id_col"):
			continue
		
		if first == True:
			insertSQL = insertSQL + i.get("name")
			place_holders = place_holders + "?"
			first = False
		else:
			insertSQL = insertSQL + ", " + i.get("name") 
			place_holders = place_holders + ", ?"
	
	insertSQL = insertSQL + ") VALUES (" + place_holders + ") RETURNING " + tab_def.get("id_col")
	
	print(insertSQL)	

# Generate UPDATE SQL
def generateUpdatedSQL(tab_def):
	
	updateSQL = "UPDATE "+tab_def.get("tab_name") +" SET "
	
	for i in tab_def.get("columns_def"):
		updateSQL = updateSQL + i.get("name") + " = ?, "
	
	updateSQL = updateSQL + "ludt = "+default_time+", luid = "+default_user
	
	updateSQL = updateSQL + " WHERE " + tab_def.get("id_col") + " = ? AND ludt = ?;"
	
	print(updateSQL)
	
# Generate UPDATE SQL
def generateUpdateStateSQL(tab_def):
	
	updateSQL = "UPDATE "+tab_def.get("tab_name") +" SET " + tab_def.get("state") + " = ?, "
	
	updateSQL = updateSQL + "ludt = "+default_time+", luid = "+default_user
	
	updateSQL = updateSQL + " WHERE " + tab_def.get("id_col") + " = ? AND ludt = ?;"
	
	print(updateSQL)

# Generate Table DDL
def generateTableDDL(tab_def):
		
	const_sql = "CREATE CONSTRAINT "
	cols = ""
	const_name = ""
	first = True
	for i in emp_tab_def.get("pk_col"):
		if first == True:
			cols = cols + i
			first = False
		else:
			cols = cols + ", " + i
		
		const_name = const_name + "_" + i
	
	seq_name = tab_def.get("tab_name")+"_"+tab_def.get("id_col")+"_seq"
	id_col = "CREATE SEQUENCE "+seq_name+" INCREMENT 1 START 1;"
	
	print(id_col)	
	
	tableDDL = "CREATE TABLE "+tab_def.get("tab_name") +"("
	
	first = True
	
	for i in tab_def.get("columns_def"):
	
		if first == True:
			tableDDL = tableDDL +i.get("name") + " "+ dtype_map.get(i.get("dtype"))
			first = False
		else:
			tableDDL = tableDDL + ", " + i.get("name") + " "+ dtype_map.get(i.get("dtype"))
	
		if i.get("dtype") == "varchar" or i.get("dtype") == "char":
			tableDDL = tableDDL + "("+str(i.get("size"))+")"
			
		if i.get("name") == tab_def.get("id_col"):
			tableDDL = tableDDL + " DEFAULT NEXTVAL('"+seq_name+"')"
		elif "default" in i:
			tableDDL = tableDDL + " DEFAULT "+i.get("default")
		
		if "notnull" in i:
			tableDDL = tableDDL + " NOT NULL"
	
	for i in strd_col:
		tableDDL = tableDDL + ", " + i.get("name") + " "+ dtype_map.get(i.get("dtype"))
		if "default" in i:
			tableDDL = tableDDL + " DEFAULT "+i.get("default")
			
	tableDDL = tableDDL + ");"
	
	print(tableDDL)	
	
	id_col = "ALTER TABLE "+tab_def.get("tab_name")+" ADD CONSTRAINT " + tab_def.get("tab_name") + const_name + "_pkey PRIMARY KEY("+cols+");"
	
	print(id_col)	


def generateSchema(tab_def):
	sch_ddl = 'CREATE SCHEMA '+tab_def.get("schema_name")+";"
	print(sch_ddl)

if __name__ == "__main__":
	print("-------------------------------------------------")
	tab_def = readTableMetadata()
	tab_name = tab_def.get("schema_name")+"."+tab_def.get("entity_name")
	tab_def["tab_name"] = tab_name
	
	generateSchema(tab_def)
	generateTableDDL(tab_def)
	print("-------------------------------------------------")
	generateSelectSQL(tab_def)
	print("-------------------------------------------------")
	generateDeleteSQL(tab_def)
	generateInsertSQL(tab_def)
	generateUpdatedSQL(tab_def)
	
	if "state" in tab_def:
		generateUpdateStateSQL(tab_def)
	
