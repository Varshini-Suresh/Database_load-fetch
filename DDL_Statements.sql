-- DDL STATEMENTS --

-- Create Subject table
CREATE TABLE Subjects (
  SubjectID VARCHAR(10) NOT NULL,
  Sex CHAR(1),
  Age DECIMAL(4,2) DEFAULT NULL,
  BMI DECIMAL(4,2) DEFAULT NULL,
  IR_IS_Classification VARCHAR(10) DEFAULT NULL,
  PRIMARY KEY (SubjectID)
);

-- Create the three OMICS Measurement tables: 
-- Create Transcriptome Abundance table
CREATE TABLE TransAbundance (
  SampleID VARCHAR(30) NOT NULL,
  SubjectID VARCHAR(10) NOT NULL,
  VisitID VARCHAR(15) NOT NULL,
  A1BGabundance DECIMAL(10,9),
  PRIMARY KEY (SubjectID, VisitID),
  FOREIGN KEY (SubjectID) REFERENCES Subject(SubjectID)
);

-- Create Proteome Abundance table
CREATE TABLE ProtAbundance (
  SampleID VARCHAR(30) NOT NULL,
  SubjectID VARCHAR(10) NOT NULL,
  VisitID VARCHAR(15) NOT NULL,
  PRIMARY KEY (SubjectID, VisitID),
  FOREIGN KEY (SubjectID) REFERENCES Subject(SubjectID)
);

-- Create Metabolome Abundance table
CREATE TABLE MetAbundance (
  SampleID VARCHAR(30) NOT NULL,
  SubjectID VARCHAR(10) NOT NULL,
  VisitID VARCHAR(15) NOT NULL,
  PRIMARY KEY (SubjectID, VisitID),
  FOREIGN KEY (SubjectID) REFERENCES Subject(SubjectID)
);

-- Create Peaks table
-- to maintain a record of unique PeakIDs 
CREATE TABLE Peaks (
  PeakID VARCHAR (50) NOT NULL,
  PRIMARY KEY (PeakID)
);

-- Create Metabolites table
-- to maintain a record of unique Metabolite identities 
CREATE TABLE Metabolites (
  MetaboliteName VARCHAR(100) NOT NULL,
  PRIMARY KEY (MetaboliteName)
);

-- Create Annotation table
-- Representing M:N relationship between Peak and Metabolite entities 
CREATE TABLE Annotation (
  PeakID VARCHAR(50) NOT NULL,
  MetaboliteName VARCHAR(100) NOT NULL,
  KEGG_ID VARCHAR(10),
  Pathway VARCHAR(255),
  PRIMARY KEY (PeakID, MetaboliteName),
  FOREIGN KEY (PeakID) REFERENCES Peaks(PeakID),
  FOREIGN KEY (MetaboliteName) REFERENCES Metabolites(MetaboliteName)
);
