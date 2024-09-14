### PARSING THE DATA FILES AND CONVERTING THEM INTO PARAMS LIST ###

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

# Merging the three annotation dict values into annotation param list - to insert into annotation table
for key, value in ann_dict.items():
    ann_param.append(value)
for key, value in ann_dict1.items():
    ann_param.append(value)
for key, value in ann_dict2.items():
    ann_param.append(value)

# print(len(ann_param)) has 738 values (724 IDs + 14 split metabolites)
print(len(comp_param))
unique_comp_param = []
for i in comp_param:
    if i not in unique_comp_param:
        unique_comp_param.append(i)
print(len(unique_comp_param))