import piplite
await piplite.install(['folium'])
await piplite.install(['pandas'])

import folium
import pandas as pd

# Import folium MarkerCluster plugin
from folium.plugins import MarkerCluster
# Import folium MousePosition plugin
from folium.plugins import MousePosition
# Import folium DivIcon plugin
from folium.features import DivIcon

# Download and read the `spacex_launch_geo.csv`
from js import fetch
import io

URL = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv'
resp = await fetch(URL)
spacex_csv_file = io.BytesIO((await resp.arrayBuffer()).to_py())
spacex_df=pd.read_csv(spacex_csv_file)

# Select relevant sub-columns: `Launch Site`, `Lat(Latitude)`, `Long(Longitude)`, `class`
spacex_df = spacex_df[['Launch Site', 'Lat', 'Long', 'class']]
launch_sites_df = spacex_df.groupby(['Launch Site'], as_index=False).first()
launch_sites_df = launch_sites_df[['Launch Site', 'Lat', 'Long']]
launch_sites_df

# Start location is NASA Johnson Space Center
nasa_coordinate = [29.559684888503615, -95.0830971930759]
site_map = folium.Map(location=nasa_coordinate, zoom_start=10)

# Create a blue circle at NASA Johnson Space Center's coordinate with a popup label showing its name
circle = folium.Circle(nasa_coordinate, radius=1000, color='#d35400', fill=True).add_child(folium.Popup('NASA Johnson Space Center'))
# Create a blue circle at NASA Johnson Space Center's coordinate with a icon showing its name
marker = folium.map.Marker(
    nasa_coordinate,
    # Create an icon as a text label
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % 'NASA JSC',
        )
    )
site_map.add_child(circle)
site_map.add_child(marker)

# Initial the map
site_map = folium.Map(location=nasa_coordinate, zoom_start=5)
# For each launch site, add a Circle object based on its coordinate (Lat, Long) values. In addition, add Launch site name as a popup label
# Create a map centered around the mean latitude and longitude of all launch sites
site_map = folium.Map(location=[spacex_df['Lat'].mean(), spacex_df['Long'].mean()], zoom_start=4)

# Iterate through each launch site
for index, row in launch_sites_df.iterrows():
    # Create a Circle object for the launch site based on its coordinates
    circle = folium.Circle(
        location=[row['Lat'], row['Long']],
        radius=1000,  # Define the radius of the circle
        color='#000000',  # Define the color of the circle
        fill=True  # Specify whether to fill the circle with color
    ).add_child(folium.Popup(row['Launch Site']))  # Add a popup label showing the launch site name
    
    # Add the Circle object to the map
    site_map.add_child(circle)
    
    # Create a Marker object for the launch site with a popup label showing its name
    marker = folium.map.Marker(
        location=[row['Lat'], row['Long']],
        icon=DivIcon(
            icon_size=(20,20),
            icon_anchor=(0,0),
            html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % row['Launch Site']
        )
    )
    
    # Add the Marker object to the map
    site_map.add_child(marker)

# Display the map
site_map

# Apply a function to check the value of `class` column
# If class=1, marker_color value will be green
# If class=0, marker_color value will be red

# Create a new column 'marker_color' in spacex_df dataframe
spacex_df['marker_color'] = spacex_df['class'].apply(lambda x: 'green' if x == 1 else 'red')
spacex_df.tail(10)

#Code is incorrect as showing only positive laucnhes
# Iterate through each row in the spacex_df dataframe
for index, row in spacex_df.iterrows():
    # Determine the cluster to add the marker based on the launch outcome
    cluster = success_cluster if row['marker_color'] == 'green' else failed_cluster
    
    # Create a Marker object for the launch with its coordinate
    marker = folium.Marker(
        location=[row['Lat'], row['Long']],  # Launch site coordinates
        popup=f"{row['Launch Site']}: {row['class']}",  # Popup label showing launch site and outcome
        icon=folium.Icon(color=row['marker_color'])  # Marker color based on marker_color column
    )
    
    # Add the Marker object to the appropriate cluster
    marker.add_to(cluster)

# Display the map
site_map

# Add Mouse Position to get the coordinate (Lat, Long) for a mouse over on the map
formatter = "function(num) {return L.Util.formatNum(num, 5);};"
mouse_position = MousePosition(
    position='topright',
    separator=' Long: ',
    empty_string='NaN',
    lng_first=False,
    num_digits=20,
    prefix='Lat:',
    lat_formatter=formatter,
    lng_formatter=formatter,
)

site_map.add_child(mouse_position)
site_map

from math import sin, cos, sqrt, atan2, radians

def calculate_distance(lat1, lon1, lat2, lon2):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance
