from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import folium
import random
import csv
import os

class GetData:    
    def __init__(self, location_name="University of Transport and Communications", 
                 num_random_points=10, max_distance_km=10, output_dir="./data/static/"):
        self.location_name = location_name
        self.num_random_points = num_random_points
        self.max_distance_km = max_distance_km
        self.output_dir = output_dir
        self.locations = []
        self.distance_matrix = []
        self.map = None
        self.lat = None
        self.lon = None
        os.makedirs(output_dir, exist_ok=True)
    
    def fetch_coordinates(self):
        geolocator = Nominatim(user_agent="map-example")
        location = geolocator.geocode(self.location_name)
        self.lat, self.lon = location.latitude, location.longitude
        self.locations = [(self.lat, self.lon)]
        return self.lat, self.lon
    
    def generate_random_point(self, base_lat, base_lon):
      dist = random.uniform(0, self.max_distance_km)
      bearing = random.uniform(0, 360)
      start = (base_lat, base_lon)
      destination = geodesic(kilometers=dist).destination(point=start, bearing=bearing)
      return destination.latitude, destination.longitude
    
    def create_map(self):
        if self.lat is None or self.lon is None:
            self.fetch_coordinates()
        self.map = folium.Map(location=[self.lat, self.lon], zoom_start=13)
        return self.map
    
    def add_markers(self):
        if self.map is None:
            self.create_map()
        
        # DEPOT's marker
        folium.Marker(
            [self.lat, self.lon],
            popup=self.location_name,
            icon=folium.Icon(color="red", icon="flag")
        ).add_to(self.map)
        
        # Points' markers
        for i, (lat, lon) in enumerate(self.locations[1:], 1):
            folium.Marker(
                [lat, lon],
                popup=f"Vị trí {i-1}",
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(self.map)
            
    def generate_random_locations(self):
        if self.lat is None or self.lon is None:
            self.fetch_coordinates()
        
        for i in range(self.num_random_points):
            r_lat, r_lon = self.generate_random_point(self.lat, self.lon)
            self.locations.append((r_lat, r_lon))
            
        return self.locations
    
    def calculate_distance_matrix(self):
        n = len(self.locations)
        self.distance_matrix = [[0.0]*n for _ in range(n)]
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    self.distance_matrix[i][j] = geodesic(self.locations[i], self.locations[j]).km
        
        return self.distance_matrix
    
    def save_map(self, filename="map.html"):
        if self.map is None:
            self.add_markers()
        
        filepath = os.path.join(self.output_dir, filename)
        self.map.save(filepath)

        
    def save_distance_matrix(self, filename="distance_matrix.csv"):
        if not self.distance_matrix:
            self.calculate_distance_matrix()
            
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, "w", newline="") as f:
            writer = csv.writer(f)
            for i, row in enumerate(self.distance_matrix):
                writer.writerow([f"{dist:.2f}" for dist in row])
        
    
    def run(self):
        self.fetch_coordinates()
        self.generate_random_locations()
        self.create_map()
        self.add_markers()
        self.calculate_distance_matrix()
        self.save_map()
        self.save_distance_matrix()
        return self.locations, self.distance_matrix