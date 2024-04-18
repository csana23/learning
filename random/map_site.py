import streamlit as st
import requests
import folium
import os

# Define a function to get weather data for a given location
def get_weather_data(location):
    api_key = os.environ.get('OPENWEATHERMAP_API_KEY')
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    return data

# Create a Streamlit app
st.title("World Weather Map")

# Get weather data for a specific location (e.g., London)
location = "London"
weather_data = get_weather_data(location)

# Extract relevant information from the weather data
temperature = weather_data["main"]["temp"] - 273.15  # Convert from Kelvin to Celsius
description = weather_data["weather"][0]["description"]
latitude = weather_data["coord"]["lat"]
longitude = weather_data["coord"]["lon"]

# Display weather information
st.write(f"Current weather in {location}:")
st.write(f"Temperature: {temperature:.2f}°C")
st.write(f"Description: {description}")

# Create a folium map centered at the specified location
m = folium.Map(location=[latitude, longitude], zoom_start=10)

# Add a marker for the location
folium.Marker([latitude, longitude], popup=f"{location}: {temperature:.2f}°C").add_to(m)

# Display the map
st.write("World Map with Weather Data")
st.write(m)
