import piplite
await piplite.install(['numpy'])
await piplite.install(['pandas'])
await piplite.install(['seaborn'])

# pandas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
#NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np
# Matplotlib is a plotting library for python and pyplot gives us a MatLab like plotting framework. We will use this in our plotter function to plot data.
import matplotlib.pyplot as plt
#Seaborn is a Python data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics
import seaborn as sns

from js import fetch
import io

#Reading the SpaceX dataset into a Pandas dataframe and print its summary
URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv"
resp = await fetch(URL)
dataset_part_2_csv = io.BytesIO((await resp.arrayBuffer()).to_py())
df=pd.read_csv(dataset_part_2_csv)
df.head(5)

#We can plot out the FlightNumber vs. PayloadMassand overlay the outcome of the launch.
#We see that as the flight number increases, the first stage is more likely to land successfully.
#The payload mass is also important; it seems the more massive the payload, the less likely the first stage will return.
sns.catplot(y="PayloadMass", x="FlightNumber", hue="Class", data=df, aspect = 5)
plt.xlabel("Flight Number",fontsize=20)
plt.ylabel("Pay load Mass (kg)",fontsize=20)
plt.show()

### TASK 1: Visualize the relationship between Flight Number and Launch Site
sns.catplot(y="LaunchSite", x="FlightNumber", data=df, aspect=3)
plt.xlabel("Flight Number", fontsize=15)
plt.ylabel("Launch Site", fontsize=15)
plt.title("Relationship between Flight Number and Launch Site", fontsize=15)
plt.show()

#Use the function catplot to plot FlightNumber vs LaunchSite, set the parameter x parameter to FlightNumber,set the y to Launch Site and set the parameter hue to 'class'
# Plot a scatter point chart with x axis to be Flight Number and y axis to be the launch site, and hue to be the class value
sns.catplot(x="FlightNumber", y="LaunchSite", hue="Class", data=df, aspect=3)
plt.xlabel("Flight Number", fontsize=15)
plt.ylabel("Launch Site", fontsize=15)
plt.title("Flight Number vs Launch Site with Class", fontsize=15)
plt.show()

### TASK 2: Visualize the relationship between Payload and Launch Site
plt.figure(figsize=(10, 6))
sns.scatterplot(x="PayloadMass", y="LaunchSite", data=df)
plt.xlabel("Payload Mass (kg)", fontsize=15)
plt.ylabel("Launch Site", fontsize=15)
plt.title("Relationship between Payload and Launch Site", fontsize=15)
plt.show()

# Plot a scatter point chart with x axis to be Pay Load Mass (kg) and y axis to be the launch site, and hue to be the class value
plt.figure(figsize=(10, 6))
sns.scatterplot(x="PayloadMass", y="LaunchSite", hue="Class", data=df)
plt.xlabel("Payload Mass (kg)", fontsize=15)
plt.ylabel("Launch Site", fontsize=15)
plt.title("Relationship between Payload Mass and Launch Site with Class", fontsize=15)
plt.show()

### TASK  3: Visualize the relationship between success rate of each orbit type

# Calculate success rate for each orbit type
orbit_success_rate = df.groupby('Orbit')['Class'].mean()

# Plot the success rate of each orbit type
plt.figure(figsize=(10, 6))
sns.barplot(x=orbit_success_rate.index, y=orbit_success_rate.values)
plt.xlabel("Orbit", fontsize=15)
plt.ylabel("Success Rate", fontsize=15)
plt.title("Success Rate of Each Orbit Type", fontsize=15)
plt.xticks(rotation=45)
plt.show()

### TASK  4: Visualize the relationship between FlightNumber and Orbit type
# Plot the relationship between FlightNumber and Orbit type
plt.figure(figsize=(10, 6))
sns.scatterplot(x='FlightNumber', y='Orbit', data=df, hue='Class')
plt.xlabel("Flight Number", fontsize=15)
plt.ylabel("Orbit", fontsize=15)
plt.title("Relationship between Flight Number and Orbit Type", fontsize=15)
plt.xticks(rotation=45)
plt.show()

# Plot a scatter point chart with x axis to be FlightNumber and y axis to be the Orbit, and hue to be the class value
# Plot the scatter point chart
plt.figure(figsize=(10, 6))
sns.scatterplot(x='FlightNumber', y='Orbit', hue='Class', data=df)
plt.xlabel("Flight Number", fontsize=15)
plt.ylabel("Orbit", fontsize=15)
plt.title("Flight Number vs Orbit with Class Hue", fontsize=15)
plt.xticks(rotation=45)
plt.show()

### TASK  5: Visualize the relationship between Payload and Orbit type
# Plot the relationship between Payload and Orbit type
plt.figure(figsize=(10, 6))
sns.scatterplot(x='PayloadMass', y='Orbit', data=df, hue='Class')
plt.xlabel("Payload Mass (kg)", fontsize=15)
plt.ylabel("Orbit", fontsize=15)
plt.title("Relationship between Payload and Orbit Type", fontsize=15)
plt.show()

# Plot a scatter point chart with x axis to be Payload and y axis to be the Orbit, and hue to be the class value
plt.figure(figsize=(10, 6))
sns.scatterplot(x='PayloadMass', y='Orbit', hue='Class', data=df)
plt.xlabel("Payload Mass (kg)", fontsize=15)
plt.ylabel("Orbit", fontsize=15)
plt.title("Payload vs Orbit with Class Hue", fontsize=15)
plt.show()

### TASK  6: Visualize the launch success yearly trend
# Extract year from Date column
df['Year'] = pd.to_datetime(df['Date']).dt.year

# Plot the launch success yearly trend
plt.figure(figsize=(12, 6))
sns.countplot(x='Year', hue='Class', data=df)
plt.xlabel("Year", fontsize=15)
plt.ylabel("Number of Launches", fontsize=15)
plt.title("Launch Success Yearly Trend", fontsize=15)
plt.legend(title='Class', loc='upper left', labels=['Failure', 'Success'])
plt.xticks(rotation=45)
plt.show()

# A function to Extract years from the date 
year=[]
def Extract_year():
    for i in df["Date"]:
        year.append(i.split("-")[0])
    return year
Extract_year()
df['Date'] = Extract_year()
df.head()

# Plot a line chart with x axis to be the extracted year and y axis to be the success rate

# Calculate success rate for each year
success_rate = df.groupby('Date')['Class'].mean()

# Plot line chart
plt.figure(figsize=(10, 6))
plt.plot(success_rate.index, success_rate.values, marker='o', linestyle='-')
plt.xlabel('Year')
plt.ylabel('Success Rate')
plt.title('Success Rate Over Years')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

#Selecting the features that will be used in success prediction in the future module
features = df[['FlightNumber', 'PayloadMass', 'Orbit', 'LaunchSite', 'Flights', 'GridFins', 'Reused', 'Legs', 'LandingPad', 'Block', 'ReusedCount', 'Serial']]
features.head()


