# %%
import folium
import pandas as pd
from folium.plugins import MiniMap, Draw
from folium.plugins import Search


class Map:
    def __init__(self, location=[41.2931, 69.2993], zoom_start=12, tiles='stamenterrain'):
        self.map = folium.Map(location=location, zoom_start=zoom_start, tiles=tiles)
        self.minimap = MiniMap(toggle_display=True)
        self.minimap.add_to(self.map)
        self.draw = Draw()
        self.draw.add_to(self.map)
        folium.TileLayer('OpenStreetMap', attr='OpenStreetMap').add_to(self.map)
        folium.TileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', name='OpenTopoMap', attr='OpenStreetMap').add_to(self.map)
        self.shapesLayer = folium.FeatureGroup(name="Stansiya")
        self.shapesLayer.add_to(self.map)
        self.bordersStyle = {
            'color': 'red',
            'weight': 2,
            'fillColor': "blue",
            'fillOpacity': 0.3
        }

    def add_marker(self, location):
        folium.Marker(location=location).add_to(self.shapesLayer)

    def add_geojson(self, geojson_path, name):
        folium.GeoJson(geojson_path, name=name, style_function=lambda x:self.bordersStyle).add_to(self.map)

    def add_layer_control(self):
        folium.LayerControl().add_to(self.map)

    def save(self, filename):
        self.map.save(filename)


class DataProcessor:
    def __init__(self, data_path):
        self.df = pd.read_excel(data_path)

    def process_data(self):
        for _, row in self.df.iterrows():
            lat, lon = row['Kenglik (°N)'], row['Uzunlik (°E)']
            Map().add_marker([lat, lon])


if __name__ == '__main__':
    map_obj = Map()
    data_processor = DataProcessor('meteostansiya.xlsx')
    data_processor.process_data()
    map_obj.add_geojson('uzbekistan_regional.geojson', 'Uzbekistan')
    map_obj.add_layer_control()
    map_obj.save('output.html')

# %%