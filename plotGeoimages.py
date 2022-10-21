"""
The script plots a map of geocoded photos (mobile phone, drone etc.) as clickable points and produces a csv table with its latitude/longitude data.

Author: Iva Mihalić (iva.mihalic@pm.me)
Date: October, 2022

Code is shared under the MIT license.
"""

import os
import folium
import pandas as pd
from exif import Image

image_folder = 'input_folder'
image_list = os.listdir(image_folder)
# Filter to use only JPG's
image_list = [image for image in image_list if image[-4:] == '.JPG' or image[-4:] == '.jpg']

# Function for getting latitude and longitude of an image
def get_latlon(image_object):
    lat_deg = image_object.gps_latitude
    lon_deg = image_object.gps_longitude
    lat_ref = image_object.gps_latitude_ref
    lon_ref = image_object.gps_longitude_ref
    lat = lat_deg[0] + lat_deg[1] / 60 + lat_deg[2] / 3600
    lon = lon_deg[0] + lon_deg[1] / 60 + lon_deg[2] / 3600
    # In case the pictures were taken in S/W hemisphere
    if lat_ref == 'S':
        lat = -lat
    if lon_ref == 'W':
        lon = -lon
    return lat, lon


# Setting up a dataframe with coordinates and photo name as an index
latlon_point = pd.DataFrame(columns=['lat', 'lon'])

for image in image_list:
    image_path = os.path.join(image_folder, image)
    with open(image_path, 'rb') as image_open:
        image_object = Image(image_open)
    lat, lon = get_latlon(image_object)
    latlon_point.loc[image, 'lat'] = lat
    latlon_point.loc[image, 'lon'] = lon

# Getting the mean values of the dataframe to center the map
center_lon = latlon_point.lon.mean()
center_lat = latlon_point.lat.mean()

# Plotting and saving the map
m = folium.Map(location=[center_lat, center_lon], zoom_start=13, control_scale=True)
for index, row in latlon_point.iterrows():
    folium.Marker(location=[row.lat, row.lon], tooltip=index, popup=index).add_to(m)

m.save('output/geophoto_map.html')
latlon_point.to_csv('output/latlon_geophoto.csv')

#comm