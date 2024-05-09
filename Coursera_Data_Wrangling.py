# Pandas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
#NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np

#Load SpaceX data
df=pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_1.csv")
df.head(10)

#Identify and calculate the percentage of the missing values in each attribute
df.isnull().sum()/len(df)*100

#Identify which columns are numerical and categorical:
df.dtypes

# Apply value_counts() on column LaunchSite
launch_counts = df['LaunchSite'].value_counts()

# Print the number of launches for each site
print(launch_counts)

# Use the method value_counts() on the column Orbit to determine the number and occurrence of each orbit
orbit_counts = df['Orbit'].value_counts()

# Print the number and occurrence of each orbit
print(orbit_counts)

# Use the method value_counts() on the column Outcome to determine the number and occurrence of each mission outcome
landing_outcomes = df['Outcome'].value_counts()

# Print the number and occurrence of each mission outcome
print(landing_outcomes)

for i,outcome in enumerate(landing_outcomes.keys()):
    print(i,outcome)

#We create a set of outcomes where the second stage did not land successfully
bad_outcomes=set(landing_outcomes.keys()[[1,3,5,6,7]])
bad_outcomes


# Using the Outcome as variable, create a list where the element is 0 if the corresponding row in Outcome is in the set bad_outcomes; otherwise, it's 1
landing_class = [0 if outcome in bad_outcomes else 1 for outcome in df['Outcome']]

df['Class']=landing_class
df[['Class']].head(15)

df.head(5)

df["Class"].mean()
