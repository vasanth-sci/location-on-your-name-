import streamlit as st
import requests
import folium
from streamlit_folium import folium_static
import pandas as pd
from typing import Tuple

class LocationIQMap:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://us1.locationiq.com/v1"
    
    def geocode(self, location: str) -> Tuple[float, float, str]:
        """
        Convert location string to coordinates using LocationIQ API
        """
        params = {
            'key': self.api_key,
            'q': location,
            'format': 'json'
        }
        
        try:
            response = requests.get(f"{self.base_url}/search.php", params=params)
            response.raise_for_status()
            data = response.json()
            
            if data and len(data) > 0:
                location_data = data[0]
                return (
                    float(location_data['lat']),
                    float(location_data['lon']),
                    location_data['display_name']
                )
            else:
                raise ValueError("No results found")
                
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to LocationIQ: {str(e)}")
            return None
        except Exception as e:
            st.error(f"Error processing location: {str(e)}")
            return None

    def create_map(self, locations: list = None, center: Tuple[float, float] = None):
        """
        Create a Folium map with markers for all locations
        """
        if center:
            initial_location = center
        elif locations and len(locations) > 0:
            initial_location = locations[0][:2]  # Use first location's coordinates
        else:
            initial_location = (40.7128, -74.0060)  # Default to New York
            
        m = folium.Map(location=initial_location, zoom_start=13)
        
        if locations:
            for lat, lon, name in locations:
                folium.Marker(
                    [lat, lon],
                    popup=name,
                    tooltip=name.split(',')[0]  # First part of address as tooltip
                ).add_to(m)
                
        return m

def main():
    st.title("LocationIQ Map Viewer")
    
    # Get API key from user input (or environment variable in production)
    api_key = st.sidebar.text_input("Enter LocationIQ API Key", type="password")
    
    if not api_key:
        st.warning("Please enter your LocationIQ API key in the sidebar")
        return
        
    map_viewer = LocationIQMap(api_key)
    
    # Search functionality
    search_col, clear_col = st.columns([3, 1])
    with search_col:
        location_input = st.text_input("Enter location to search", key="location_search")
    with clear_col:
        if st.button("Clear"):
            st.session_state.locations = []
            st.experimental_rerun()
    
    # Initialize session state for storing locations
    if 'locations' not in st.session_state:
        st.session_state.locations = []
    
    # Search button
    if st.button("Search") and location_input:
        result = map_viewer.geocode(location_input)
        if result:
            st.session_state.locations.append(result)
    
    # Display locations table if we have any
    if st.session_state.locations:
        df = pd.DataFrame(
            st.session_state.locations,
            columns=['Latitude', 'Longitude', 'Address']
        )
        st.dataframe(df)
    
    # Create and display map
    if st.session_state.locations:
        m = map_viewer.create_map(locations=st.session_state.locations)
    else:
        m = map_viewer.create_map()
    
    # Display the map
    folium_static(m)

if __name__ == "__main__":
    main()