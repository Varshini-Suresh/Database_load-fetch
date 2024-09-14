### MAIN PYTHON FILE FOR CW 2 ###
# Import statements
import argparse
from db_classes import Database
import matplotlib.pyplot as plot

## SETTING UP ARGPARSER ## 
parser = argparse.ArgumentParser(description='CREATE, LOAD AND QUERY A DATABASE DESIGNED TO STORE OMICS DATA FROM PATIENTS',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("--createdb", required=False, action='store_true', help='Create a database structure')
parser.add_argument('--loaddb', required=False, action='store_true', help="Parse and insert relevant data into the database")
parser.add_argument('--querydb', required=False, type=int, choices=range(1,10), help="Use an option from 1-9 to run a specific query")
parser.add_argument('db_file', help="Name of the database file")

args = parser.parse_args()


#### CREATING THE DATABASE SCHEMA ####
# Specifying argparse input file as db file in Database class 
db_file = args.db_file

# ARGPARSE - Specifying the arguments for createdb method: 
if args.createdb:
    try:
        with open('DDL_statements.sql', 'r') as sql_script:
            sql_script = sql_script.read()
        create = Database.create_db(db_file, sql_script)
    except FileNotFoundError:
        print(f'File {sql_script} not found. Please check and try again.')

#### LOADING THE DATABASE ####
## PARSING THE DATA FILES AND CONVERTING THEM INTO PARAMS LIST ##
# Parsing the Subjects table from Subject.csv
subjects_dict = {} # dictionary to store parsed data
try: 
    with open('Subject.csv') as sub_file: 
        header = next(sub_file)
        for line in sub_file:
            line = line.rstrip().split(',')
            # replacing NAs and Unknowns with None
            for i in range(0, len(line)): 
                if line[i] == 'NA' or line[i] == 'Unknown':
                    line[i] = None
            SubjectID = line[0]
            Sex = line[2]
            Age = line[3]
            BMI = line[4]
            IR_IS_Classification = line[6]
            subjects_dict[SubjectID] = [SubjectID, Sex, Age, BMI, IR_IS_Classification]
except FileNotFoundError: 
    print(f'File {sub_file} not found. Please try again')

subject_params = [] # storing dict values as a list of parameter values 
for key, value in subjects_dict.items():
    subject_params.append(value)

### Parsing the three OMICS Measurements tables 
# Transcriptome Abundance 
trans_dict, pro_dict, met_dict = {}, {}, {} 
try: 
    with open('HMP_transcriptome_abundance.tsv') as trans_file: 
        header = next(trans_file)
        for row in trans_file:
            row = row.rstrip().split('\t')
            SampleID = row[0]
            SubjectID = SampleID.split('-')[0]
            VisitID = SampleID.split('-')[1]
            A1BG = row[1]
            trans_dict[SampleID] = [SampleID, SubjectID, VisitID, A1BG]
except FileNotFoundError:
    print(f'File {trans_file} not found. Please check and try again.')

# Proteome Abundance 
try: 
    with open('HMP_proteome_abundance.tsv') as pro_file: 
        header = next(pro_file)
        for row in pro_file:
            row = row.rstrip().split('\t')
            SampleID = row[0]
            SubjectID = SampleID.split('-')[0]
            VisitID = SampleID.split('-')[1]
            pro_dict[SampleID] = [SampleID, SubjectID, VisitID]
except FileNotFoundError:
    print(f'File {pro_file} not found. Please check and try again.')  

# Metabolome Abundance 
try: 
    with open('HMP_metabolome_abundance.tsv') as met_file: 
        header = next(met_file)
        for row in met_file:
            row = row.rstrip().split('\t')
            SampleID = row[0]
            SubjectID = SampleID.split('-')[0]
            VisitID = SampleID.split('-')[1]
            met_dict[SampleID] = [SampleID, SubjectID, VisitID]
except FileNotFoundError:
    print(f'File {met_file} not found. Please check and try again.')

# Appending dict values of omics to params list to load into the 3 omics tables in the DB 
trans_params, pro_params, met_params = [], [], []
for key, value in trans_dict.items():
    trans_params.append(value)
for key, value in pro_dict.items():
    pro_params.append(value)
for key, value in met_dict.items():
    met_params.append(value)


# Parsing Metabolome Annotation table into Peaks and Annotation tables 
peaks_dict, ann_dict, ann_dict1, ann_dict2 = {}, {}, {}, {}
comp_dict, comp_dict1, comp_dict2 = {}, {}, {}
try: 
    with open('HMP_metabolome_annotation.csv') as peak_file: 
        header = next(peak_file)
        for row in peak_file:
            row = row.rstrip().split(',')
            PeakID = row[0]
            peaks_dict[PeakID] = [PeakID]
            Metabolite = row[1]
            KEGG = row[2]
            Pathway = row[5]
            # Removing suffix for metabolites 
            suffix = ("(1)", "(2)", "(3)", "(4)", "(5)")
            if Metabolite.endswith(suffix):
                Metabolite = Metabolite[:-3]
            # Spliting KEGG and Metabolites with "|" as two
            if "|" in KEGG:
                KEGG1 = row[2].split('|')[0]
                KEGG2 = row[2].split('|')[1]
            if "|" in Metabolite:
                Metabolite1 = row[1].split('|')[0]
                Metabolite2 = row[1].split('|')[1]
                comp_dict1[Metabolite1] = [Metabolite1]
                comp_dict2[Metabolite2] = [Metabolite2]
                # Storing the same Peak and Pathway info for each Metabolite and KEGG
                ann_dict1[PeakID] = [PeakID, Metabolite1, KEGG1, Pathway]
                ann_dict2[PeakID] = [PeakID, Metabolite2, KEGG2, Pathway]
            else: 
                ann_dict[PeakID] = [PeakID, Metabolite, KEGG, Pathway]
                comp_dict[Metabolite] = [Metabolite]
except FileNotFoundError:
    print(f'File {peak_file} not found. Please check and try again.')

# For Peaks ID table 
peaks_param, ann_param, comp_param = [], [], [] # creating empty param lists for subsequent INSERT statements
for key, value in peaks_dict.items():
    peaks_param.append(value)

# Merging the three metabolite compound dictionaries into compound param list - for metabolite table
for key, value in comp_dict.items():
    comp_param.append(value)
for key, value in comp_dict1.items():
    comp_param.append(value)
for key, value in comp_dict2.items():
    comp_param.append(value)
unique_comp_param = [] # to store just unique metabolite identifiers 
for i in comp_param:
    if i not in unique_comp_param:
        unique_comp_param.append(i)

# Merging the three annotation dict values into annotation param list - to insert into annotation table
for key, value in ann_dict.items():
    ann_param.append(value)
for key, value in ann_dict1.items():
    ann_param.append(value)
for key, value in ann_dict2.items():
    ann_param.append(value)

    
## LOADING THE DATABASE USING INSERT STATEMENTS ##
# The insert statements for each of the tables
subject_insert = "INSERT INTO Subjects VALUES (?, ?, ?, ?, ?);"
trans_insert = "INSERT INTO TransAbundance VALUES (?, ?, ?, ?)"
pro_insert = "INSERT INTO ProtAbundance VALUES (?, ?, ?)"
met_insert = "INSERT INTO MetAbundance VALUES (?, ?, ?)"
peak_insert = "INSERT INTO Peaks VALUES (?)"
comp_insert = "INSERT INTO Metabolites VALUES (?)"
ann_insert = "INSERT INTO Annotation VALUES (?, ?, ?, ?)"

# ARGPARSE - Specifying arguments for the loaddb option 
if args.loaddb:
    sub_load = Database.insert_db(db_file, subject_insert, subject_params)
    trans_load = Database.insert_db(db_file, trans_insert, trans_params)
    pro_load = Database.insert_db(db_file, pro_insert, pro_params)
    met_load = Database.insert_db(db_file, met_insert, met_params)
    peak_load = Database.insert_db(db_file, peak_insert, peaks_param)
    comp_load = Database.insert_db(db_file, comp_insert, unique_comp_param)
    ann_load = Database.insert_db(db_file, ann_insert, ann_param)


#### QUERYING FROM THE DATABASE ####
## SQLITE3 SELECT STATEMENTS FOR QUERIES 1-9 ##
# sql select statements 
sql1 = "SELECT Subjects.SubjectID, Subjects.Age FROM Subjects WHERE Subjects.Age > 70;"
sql2 = "SELECT Subjects.SubjectID FROM Subjects WHERE Subjects.Sex LIKE 'F' \
      AND Subjects.BMI BETWEEN 18.5 AND 24.9 ORDER BY Subjects.SubjectID DESC;"

sql3 = "SELECT TransAbundance.VisitID FROM TransAbundance WHERE TransAbundance.SubjectID LIKE 'ZNQOVZV' \
UNION ALL SELECT ProtAbundance.VisitID FROM ProtAbundance WHERE ProtAbundance.SubjectID LIKE 'ZNQOVZV'\
UNION ALL SELECT MetAbundance.VisitID FROM MetAbundance WHERE MetAbundance.SubjectID LIKE 'ZNQOVZV';"

sql4 = "SELECT DISTINCT MetAbundance.SubjectID FROM MetAbundance INTERSECT SELECT Subjects.SubjectID FROM Subjects WHERE Subjects.IR_IS_Classification LIKE 'IR';"
sql5 = "SELECT DISTINCT Annotation.KEGG_ID FROM Annotation WHERE Annotation.PeakID IN (?, ?, ?, ?);"
sql6 = "SELECT MIN(Subjects.Age) AS Min_Age, MAX(Subjects.Age) AS Max_Age, AVG(Subjects.Age) AS Avg_Age FROM Subjects;"

sql7 = "SELECT Annotation.Pathway, COUNT(Annotation.Pathway) AS Count FROM Annotation WHERE Annotation.Pathway NOT LIKE ''\
GROUP BY Annotation.Pathway HAVING COUNT(Annotation.Pathway) > 10 ORDER BY COUNT(Annotation.Pathway) DESC;"
sql8 = "SELECT MAX(TransAbundance.A1BGabundance) AS Max_A1BG FROM TransAbundance WHERE TransAbundance.SubjectID LIKE 'ZOZOW1T';"
sql9 = "SELECT Subjects.Age, Subjects.BMI FROM Subjects WHERE Subjects.Age IS NOT NULL AND Subjects.BMI IS NOT NULL;"

# parameterised statements 
param = [] # most queries here are unparameterised statements, hence can be empty
param5 = ["nHILIC_121.0505_3.5","nHILIC_130.0872_6.3","nHILIC_133.0506_2.3","nHILIC_133.0506_4.4"] # for sql query 5 

# ARGPARSE - Specifying each argument for querydb options 1-9 
if args.querydb==1:
    query = Database.query_db(db_file, sql1, param)
    for row in query:
        print(f'{row[0]}\t{row[1]}') # 2 output columns 
if args.querydb==2:
    query = Database.query_db(db_file, sql2, param)
    for row in query:
        print(f'{row[0]}')
if args.querydb==3:
    query = Database.query_db(db_file, sql3, param)
    for row in query:
        print(f'{row[0]}')
if args.querydb==4:
    query = Database.query_db(db_file, sql4, param)
    for row in query:
        print(f'{row[0]}')
if args.querydb==5:
    query = Database.query_db(db_file, sql5, param5)
    for row in query:
        print(f'{row[0]}')
if args.querydb==6:
    query = Database.query_db(db_file, sql6, param) 
    for row in query:
        print(f'{row[0]}\t{row[1]}\t{row[2]}')
if args.querydb==7:
    query = Database.query_db(db_file, sql7, param)
    for row in query:
        print(f'{row[0]}')
if args.querydb==8:
    query = Database.query_db(db_file, sql8, param)
    for row in query:
        print(f'{row[0]}')
age_x, bmi_y = [], []
if args.querydb==9:
    query = Database.query_db(db_file, sql9, param)
    for row in query:
        age, bmi = row[0], row[1]
        age_x.append(age)
        bmi_y.append(bmi)
        print(f'{row[0]}\t{row[1]}')
    plot.scatter(x=age_x, y=bmi_y)
    plot.title("Age vs BMI")
    plot.xlabel("Age")
    plot.ylabel("BMI")
    plot.savefig("age_bmi_scatterplot.png")

