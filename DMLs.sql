SELECT Subjects.SubjectID, Subjects.Age FROM Subjects
WHERE Subjects.Age > 70;

SELECT Subjects.SubjectID FROM Subjects
WHERE Subjects.Sex LIKE 'F' AND Subjects.BMI BETWEEN 18.5 AND 24.9
ORDER BY Subjects.SubjectID DESC;

SELECT TransAbundance.VisitID FROM TransAbundance
WHERE TransAbundance.SubjectID LIKE 'ZNQOVZV'
UNION ALL
SELECT ProtAbundance.VisitID FROM ProtAbundance
WHERE ProtAbundance.SubjectID LIKE 'ZNQOVZV'
UNION ALL
SELECT MetAbundance.VisitID FROM MetAbundance
WHERE MetAbundance.SubjectID LIKE 'ZNQOVZV';

SELECT DISTINCT MetAbundance.SubjectID FROM MetAbundance
INTERSECT
SELECT Subjects.SubjectID FROM Subjects WHERE Subjects.IR_IS_Classification LIKE 'IR';

SELECT DISTINCT Annotation.KEGG_ID FROM Annotation
WHERE Annotation.PeakID IN ("nHILIC_121.0505_3.5","nHILIC_130.0872_6.3","nHILIC_133.0506_2.3","nHILIC_133.0506_4.4");

SELECT MIN(Subjects.Age) AS Min_Age,
       MAX(Subjects.Age) AS Max_Age,
       AVG(Subjects.Age) AS Avg_Age
FROM Subjects;

SELECT Annotation.Pathway, COUNT(Annotation.Pathway) AS Count 
FROM Annotation 
WHERE Annotation.Pathway NOT LIKE ''
GROUP BY Annotation.Pathway
HAVING COUNT(Annotation.Pathway) > 10
ORDER BY COUNT(Annotation.Pathway) DESC;

SELECT MAX(TransAbundance.A1BGabundance) AS Max_A1BG
FROM TransAbundance
WHERE TransAbundance.SubjectID LIKE 'ZOZOW1T';

SELECT Subjects.Age, Subjects.BMI FROM Subjects
WHERE Subjects.Age IS NOT NULL 
AND Subjects.BMI IS NOT NULL;





