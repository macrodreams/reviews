import streamlit as st
import requests

API_KEY = "YOUR_GOOGLE_API_KEY"  # Ensure to use your actual API key

# Function to get place ID based on the name and location
def get_place_id(name, lat, lng):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "key": API_KEY,
        "location": f"{lat},{lng}",
        "radius": 100,
        "keyword": name
    }
    response = requests.get(url, params=params)
    results = response.json().get("results", [])
    if results:
        return results[0]["place_id"]
    return None

# Function to get reviews using place ID
def get_reviews(place_id):
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "key": API_KEY,
        "place_id": place_id,
        "fields": "rating,reviews"
    }
    response = requests.get(url, params=params)
    return response.json().get("result", {})

# Streamlit interface for custom prompt
st.title("Fetch Reviews and Ratings Dynamically")

st.sidebar.header("Enter Location Details")
place_name = st.sidebar.text_input("Enter the EV Charging Station Name (e.g., ChargePoint Charging Station)", "")
latitude = st.sidebar.number_input("Enter Latitude", value=37.339623)  # Default: San Jose, CA
longitude = st.sidebar.number_input("Enter Longitude", value=-121.896821)  # Default: San Jose, CA

submit = st.sidebar.button("Submit Query")

if submit:
    if place_name and latitude and longitude:
        st.write(f"Fetching reviews for **{place_name}** located at ({latitude}, {longitude})...")

        # Fetch place ID
        place_id = get_place_id(place_name, latitude, longitude)
        if place_id:
            # Fetch reviews for the place
            details = get_reviews(place_id)
            if details.get("reviews"):
                st.write("⭐ Rating:", details.get("rating"))
                st.write("🗣️ Sample Review:", details["reviews"][0].get("text", "No review available"))
            else:
                st.write("No reviews found for this location.")
        else:
            st.write("Place not found. Please check the name or coordinates and try again.")
    else:
        st.write("Please provide a location name and coordinates.")
