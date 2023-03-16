# %%
import folium
import pandas as pd
from folium.plugins import MiniMap
from folium.plugins import Draw


mapObj = folium.Map(location=[41.2931, 69.2993],
                    zoom_start=12, tiles='stamenterrain')

minimap = MiniMap(toggle_display=True)
minimap.add_to(mapObj)

draw = Draw()

draw.add_to(mapObj)

folium.TileLayer('OpenStreetMap',
            attr='OpenStreetMap').add_to(mapObj)

folium.TileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
            name = 'OpenTopoMap',
            attr='OpenStreetMap').add_to(mapObj)

shapesLayer = folium.FeatureGroup(name="Stansiya").add_to(mapObj)
df = pd.read_excel('meteostansiya.xlsx')

for itr in range(len(df)):
    wm = df.iloc[itr]["WMO_ID"]
    joy = df.iloc[itr]["Joylashgan hududi"]
    ModuleNotFoundError = df.iloc[itr]["Meteostansiyalar nomi"]
    keng = df.iloc[itr]["Kenglik (°N)"]
    uzun = df.iloc[itr]["Uzunlik (°E)"]
    dsb = df.iloc[itr]["Dengiz satxidan balandligi (m)"]
    kd = df.iloc[itr]["Kuzatuv davri"]
    folium.Marker(
        location=[keng, uzun]
    ).add_to(shapesLayer)

# folium.Marker(location=[41.3192, 69.3062]).add_to(mapObj)

bordersStyle={
    'color': 'red',
    'weight': 2,
    'fillColor': "blue",
    'fillOpacity': 0.3
}

folium.GeoJson("uzbekistan_regional.geojson", 
               name="Uzbekistan",
               style_function=lambda x:bordersStyle).add_to(mapObj)

folium.LayerControl().add_to(mapObj)

mapObj.save('output.html')
# %%