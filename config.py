"""
This file contains a configurations/credentials used in project

================================================================
The db_string variable stores the connection string that provides
the necessary credentials and information to connect to a database.
Pattern for db_string:
"database_type://user:password@database_url:port/database_name"
This string includes details such as:
- database type <- postgresql, 
- username <- postgres, 
- password <- password, 
- host <- localhost, 
- port <- 5432,
- database name <- postgres
================================================================
"""

db_string = "postgresql://postgres:password@localhost:5432/postgres"