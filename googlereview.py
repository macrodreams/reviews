import streamlit as st
import requests

API_KEY = "YOUR_GOOGLE_API_KEY"  # Ensure to use your actual API key

# Function to get place ID based on the name and location
def get_place_id(name, lat, lng):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "key": API_KEY,
        "location": f"{lat},{lng}",
        "radius": 10000,  # Further increased radius to 10000 meters
        "keyword": name,
        "type": "charging_station"  # Filter for charging stations
    }
    response = requests.get(url, params=params)
    results = response.json().get("results", [])

    # Debug log: Show the raw results returned by Google
    st.json(response.json())  # Display the full raw response for debugging

    if not results:
        st.warning("No places found nearby. Try adjusting the name or increasing the radius.")
    else:
        st.success(f"Found {len(results)} place(s). Top match: {results[0]['name']}")

    return results[0]["place_id"] if results else None

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
latitude = st.sidebar.text_input("Enter Latitude", value="37.339623")  # Default: San Jose, CA
longitude = st.sidebar.text_input("Enter Longitude", value="-121.896821")  # Default: San Jose, CA

submit = st.sidebar.button("Submit Query")

if submit:
    if place_name and latitude and longitude:
        try:
            lat = float(latitude)
            lng = float(longitude)

            st.write(f"Fetching reviews for **{place_name}** located at ({lat}, {lng})...")

            # Fetch place ID
            place_id = get_place_id(place_name, lat, lng)
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
        except ValueError:
            st.error("Please enter valid numeric values for Latitude and Longitude.")
    else:
        st.write("Please provide a location name and coordinates.")
