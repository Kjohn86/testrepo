!pip install sqlalchemy==1.3.9
%load_ext sql

import csv, sqlite3

con = sqlite3.connect("my_data1.db")
cur = con.cursor()

!pip install -q pandas==1.1.5
%sql sqlite:///my_data1.db

import pandas as pd
df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv")
df.to_sql("SPACEXTBL", con, if_exists='replace', index=False,method="multi")

#Removing blanks from the table
%sql create table SPACEXTABLE as select * from SPACEXTBL where Date is not null

# Execute the SQL query
cur.execute("SELECT DISTINCT Launch_Site FROM SPACEXTABLE")

# Fetch all the rows of the result
rows = cur.fetchall()

# Print the unique launch sites
for row in rows:
    print(row[0])

# Execute the SQL query to select 5 records where launch sites begin with 'CCA'
cur.execute("SELECT * FROM SPACEXTABLE WHERE Launch_Site LIKE 'CCA%' LIMIT 5")

# Fetch all the rows of the result
rows = cur.fetchall()

# Print the selected records
for row in rows:
    print(row)

cur.execute("""
    SELECT SUM(PAYLOAD_MASS__KG_)
    FROM SPACEXTABLE
    WHERE Customer = 'NASA (CRS)'
""")

# Fetch the result of the query
total_payload_mass = cur.fetchone()[0]

# Print the total payload mass
print("Total payload mass carried by boosters launched by NASA (CRS):", total_payload_mass)

# Execute the SQL query to calculate the average payload mass carried by booster version F9 v1.1
cur.execute("""
    SELECT AVG(PAYLOAD_MASS__KG_)
    FROM SPACEXTABLE 
    WHERE Booster_Version = 'F9 v1.1'
""")

# Fetch the result of the query
average_payload_mass = cur.fetchone()[0]

# Print the average payload mass
print("Average payload mass carried by booster version F9 v1.1:", average_payload_mass)

# Execute the SQL query to select the boosters that have success in drone ship and have payload mass greater than 4000 but less than 6000
cur.execute("""
    SELECT DISTINCT Booster_Version
    FROM SPACEXTABLE 
    WHERE Landing_Outcome = 'Success (drone ship)'
    AND PAYLOAD_MASS__KG_ > 4000
    AND PAYLOAD_MASS__KG_ < 6000
""")

# Fetch all the rows of the result
rows = cur.fetchall()

# Print the names of the boosters
for row in rows:
    print(row[0])

# Execute the SQL query to count the total number of successful mission outcomes
cur.execute("""
    SELECT COUNT(*)
    FROM SPACEXTABLE
    WHERE Mission_Outcome = 'Success'
""")

# Fetch the result of the query
success_count = cur.fetchone()[0]

# Print the total number of successful mission outcomes
print("Total number of successful mission outcomes:", success_count)

# Execute the SQL query to count the total number of failure mission outcomes
cur.execute("""
    SELECT COUNT(*) 
    FROM SPACEXTABLE 
    WHERE Mission_Outcome = 'Failure (in flight)'
""")

# Fetch the result of the query
failure_count = cur.fetchone()[0]

# Print the total number of failure mission outcomes
print("Total number of failure mission outcomes:", failure_count)

# Execute the SQL query with a subquery to find the maximum payload mass
cur.execute("""
    SELECT Booster_Version
    FROM SPACEXTABLE
    WHERE PAYLOAD_MASS__KG_ = (
        SELECT MAX(PAYLOAD_MASS__KG_)
        FROM SPACEXTABLE
    )
""")

# Fetch all the rows of the result
rows = cur.fetchall()

# Print the names of the booster_versions
for row in rows:
    print(row[0])

# Execute the SQL query to select the records meeting the specified criteria
cur.execute("""
    SELECT
        CASE
            WHEN substr(Date, 6, 2) = '01' THEN 'January'
            WHEN substr(Date, 6, 2) = '02' THEN 'February'
            WHEN substr(Date, 6, 2) = '03' THEN 'March'
            WHEN substr(Date, 6, 2) = '04' THEN 'April'
            WHEN substr(Date, 6, 2) = '05' THEN 'May'
            WHEN substr(Date, 6, 2) = '06' THEN 'June'
            WHEN substr(Date, 6, 2) = '07' THEN 'July'
            WHEN substr(Date, 6, 2) = '08' THEN 'August'
            WHEN substr(Date, 6, 2) = '09' THEN 'September'
            WHEN substr(Date, 6, 2) = '10' THEN 'October'
            WHEN substr(Date, 6, 2) = '11' THEN 'November'
            WHEN substr(Date, 6, 2) = '12' THEN 'December'
        END AS Month,
        Landing_Outcome,
        Booster_Version,
        Launch_Site
    FROM SPACEXTABLE
    WHERE substr(Date, 0, 5) = '2015'
    AND Landing_Outcome LIKE 'Failure%'
    AND Landing_Outcome LIKE '%drone ship%'
""")

# Fetch all the rows of the result
rows = cur.fetchall()

# Print the records
for row in rows:
    print(row)

# Execute the SQL query to rank the count of landing outcomes between the specified dates
cur.execute("""
    SELECT
        Landing_Outcome,
        COUNT(*) AS OutcomeCount
    FROM SPACEXTABLE
    WHERE Date BETWEEN '2010-06-04' AND '2017-03-20'
    AND Landing_Outcome IN ('Failure (drone ship)', 'Success (ground pad)')
    GROUP BY Landing_Outcome
    ORDER BY OutcomeCount DESC
""")

# Fetch all the rows of the result
rows = cur.fetchall()

# Print the ranked count of landing outcomes
for row in rows:
    print(row)
