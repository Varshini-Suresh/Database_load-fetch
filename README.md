# Bioinformatics Database with Load and Fetch Utility using Python

## Project Outline 
The main objective of the program was to design, create and load a database based on the given data files, 
and establish a connection with the database to interact with the database and perform certain queries. 

## Datafiles 
The datafiles (in .csv format) that were provided include:</br> 
(1)	Information on 106 subjects of the study, such as age, BMI, insulin resistance, etc</br>
(2)	Proteome abundance for each patient from each clinical visit</br>
(3)	Transcriptome abundance for each patient from each clinical visit</br>
(4)	Metabolome abundance for each patient from each clinical visit</br>
(5)	Annotations of the metabolome based on KEGG pathway</br>


## Scripts 
The scripts used throughout the project was:</br> 
(1)	**db_classes.py:** Three classes were created with different functions to: create, load, and fetch data from a database based on the datafiles provided.  
*create_db:* Creates a database schema based on given SQLite3 DDL statements, found in the ‘DDL_Statements.sql’</br>
*insert_db:* Executes a single INSERT statement. Specifying multiple params will allow multiple records to be inserted in one go</br>
*query_db:* Executes a specified SELECT statement on the created database. The 9 query statements written in SQL are outlined in ‘DMLs.sql’.</br></br>
(2)	**load.py:** This script aids with parsing the given .csv datafiles by only storing selected fields into the designed database as dictionaries and turning the values into a list that can be substituted with the parameter placeholders (denoted with the “?” sign).</br> </br>
(3)	**main.py:** This script brings in the Database classes, the SQL scripts and the DB parser script (load.py) into one to perform all three utilities, as mentioned below:</br> 
```
usage: main.py [-h] [--createdb] [--loaddb] [--querydb {1,2,3,4,5,6,7,8,9}] db_file

CREATE, LOAD AND QUERY A DATABASE DESIGNED TO STORE OMICS DATA FROM PATIENTS

positional arguments:
  db_file               Name of the database file

options:
  -h, --help            show this help message and exit
  --createdb            Create a database structure (default: False)
  --loaddb              Parse and insert relevant data into the database (default: False)
  --querydb {1,2,3,4,5,6,7,8,9}
                        Use an option from 1-9 to run a specific query (default: None)
```
