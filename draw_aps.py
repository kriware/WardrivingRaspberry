import pandas as pd
import folium
from folium import Map, Marker

wd = pd.read_csv ('<your_CSV_file_from_netxml_to_csv_script>')

basic_map = folium.Map(location=[<YOUR_LOCATION_LAT>, <YOUR_LOCATION_LONG>],zoom_start=16)

wd = pd.DataFrame( wd.loc[wd['Encryption'] == "WEP"] ) # filter by WEP
wd = wd.reset_index(drop=True)

for i in range(len(wd)): 
  lat = wd["Latitude"][i]
  lon = wd["Longitude"][i] 
  folium.Marker( location=[lat, lon], popup=wd["SSID"][i], icon=folium.Icon(icon="wifi", prefix='fa') ).add_to(basic_map)


display(basic_map)
