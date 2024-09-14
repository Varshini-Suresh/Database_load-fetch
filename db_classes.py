### CLASS AND METHODS REQUIRED FOR DATABSE INTERACTION ###

import sqlite3

# Create a DB class 
class Database: 
    def __init__(self, db_file):
        self._db_file = db_file
    
    # Method to CREATE db 
    def create_db(db_file, sql_script):
        """
        Creates a database schema based on given SQLite3 DDL statements 
        Parameters: 
        db_file: file path of the SQLite 3 database file (string)
        sql_script: the DDL statements required to create the schema ('.sql' text file)
        Returns nothing on terminal but database schema gets created in the same directory 
        """
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        cursor.executescript(sql_script)
        connection.commit()
        cursor.close()
        connection.close()


    # Method to LOAD db 
    def insert_db(db_file, inserts, params): 
        """
        Executes a single INSERT statement
        Specifying multiple params will allow multiple records to be inserted in 1 go
        Parameters:
        db_file: file path of the SQLite3 database file (string)
        sql: the INSERT statements to be executed (string)
        params: parameters to be substituted in the INSERT statements (list or tuple)
        Returns nothing 
        """
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        cursor.executemany(inserts, params) # no need for result here, as there are no returns 
        connection.commit()
        cursor.close()
        connection.close()


    # Method to QUERY db 
    def query_db(db_file, sql_query, param): 
        """
        Executes a specified select statement for the given DB file
        Parameters: 
        db_file: file path of the SQLite3 database file (string)
        sql_query: the SELECT statements to be executed from the database (string)
        params: parameters to be substituted in the sql query (list or tuple) 
        if parameter subtitutions is required, then sql_query to be written with placeholders('?,?,?..')
        Returns a list of tuples containing results to the sql query 
        """
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        result = cursor.execute(sql_query, param).fetchall()
        cursor.close()
        connection.close()
        return result

