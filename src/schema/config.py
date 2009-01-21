#                      DATABASE CONFIGURATION
#---------------------------------------------------------------------
# The DBMS name "Database management system" (example: mysql, postres)
# DBMS= "oracle"
#DBMS= "postgres"
DBMS= "mysql"
# Data base name
db_name = "test"
# Badabase Host
db_host = "172.22.1.247"
# Data base connection port
#db_port = "5432" # postgres default port
db_port = "3306" # mysql default port
# Data_base user_name
#db_user = "root"
db_user = "gioby"
# Data_base password
db_password= ""
# ********************************************************** 

connection_line = "%s://%s@%s:%s/%s" % (DBMS, db_user, db_host, db_port, db_name)
