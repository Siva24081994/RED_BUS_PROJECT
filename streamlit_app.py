import streamlit as st
import mysql.connector
import pandas as pd

# Title of the app
st.markdown("<h1 style='color: red; font-weight: bold;'>Redbus</h1>", unsafe_allow_html=True)

# MySQL connection setup
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Replace with your MySQL root password
        database="RED_BUS"
    )

# Function to filter data based on user input
def filter_data(state, route, bus_type, bus_name, price_range, star_rating_range, seat_availability, depart_time=None, reach_time=None):
    query = "SELECT * FROM RED_BUS_R WHERE 1=1"
    params = []

    # State filter
    if state:
        query += " AND state = %s"
        params.append(state)

    # Route filter
    if route:
        query += " AND route_name IN (%s)" % ','.join(['%s'] * len(route))
        params.extend(route)

    # Bus type filter (A/C or Non-A/C based on radio button)
    if bus_type == 'A/C':
        query += " AND bustype = 'A/C'"  # Match exactly "A/C"
    elif bus_type == 'NON A/C':
        query += " AND bustype = 'NON A/C'"  # Match exactly "Non A/C"



    # Bus name filter
    if bus_name:
        query += " AND busname IN (%s)" % ','.join(['%s'] * len(bus_name))
        params.extend(bus_name)

    # Price range filter
    query += " AND price BETWEEN %s AND %s"
    params.extend(price_range)

    # Star rating filter
    if star_rating_range[0] > 0.0 or star_rating_range[1] < 5.0:
        query += " AND star_rating BETWEEN %s AND %s"
        params.extend(star_rating_range)

    # Seat availability filter
    if seat_availability > 0:
        query += " AND seats_available >= %s"
        params.append(seat_availability)

    # Departing time filter
    if depart_time is not None:
        query += " AND departing_time >= %s"
        params.append(depart_time)

    # Reaching time filter
    if reach_time is not None:
        query += " AND reaching_time <= %s"
        params.append(reach_time)

    return query, params

# Fetch data from MySQL database based on query
def load_data(query, params=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(rows, columns=columns)
    conn.close()
    return df

# Sidebar filters
st.sidebar.header("Filter Options")

# State Filter
states = load_data("SELECT DISTINCT state FROM RED_BUS_R")
state_filter = st.sidebar.selectbox("State", states['state'])

# Route Name Filter (filtered based on the selected state)
if state_filter:
    routes = load_data("SELECT DISTINCT route_name FROM RED_BUS_R WHERE state = %s", [state_filter])
    route_filter = st.sidebar.multiselect("Route Name", routes['route_name'])
else:
    route_filter = []

# Bus Type Filter (using radio buttons)
bus_type_filter = st.sidebar.radio("Bus Type", ['A/C', 'NON A/C'])  # A/C or Non A/C

# Bus Name Filter (filtered based on the selected state)
bus_names = load_data("SELECT DISTINCT busname FROM RED_BUS_R WHERE state = %s", [state_filter])
bus_name_filter = st.sidebar.multiselect("Bus Name", bus_names['busname'])

# Price Range Filter
price_min, price_max = load_data("SELECT MIN(price), MAX(price) FROM RED_BUS_R WHERE state = %s", [state_filter]).iloc[0]
price_range_filter = st.sidebar.slider("Price Range", float(price_min), float(price_max), (float(price_min), float(price_max)))

# Star Rating Filter (double-sided slider for a range)
star_rating_range_filter = st.sidebar.slider("Star Rating Range", 0.0, 5.0, (0.0, 5.0))

# Seat Availability Filter
seat_availability_filter = st.sidebar.slider("Minimum Seats Available", 0, 50, 0)

# Time Selection Filters for Departing and Reaching
depart_time_filter = st.sidebar.time_input("Select Departing Time", None)
reach_time_filter = st.sidebar.time_input("Select Reaching Time", None)

# Convert times to 24-hour format (if None, pass None to avoid filtering by time)
def time_to_24hr(time_input):
    return time_input.strftime('%H:%M') if time_input is not None else None

# Filter data based on user input
query, params = filter_data(state_filter, route_filter, bus_type_filter, bus_name_filter, price_range_filter, star_rating_range_filter, seat_availability_filter, time_to_24hr(depart_time_filter), time_to_24hr(reach_time_filter))
filtered_data = load_data(query, params)

# Display filtered data
st.write("### Filtered Bus Data")
st.dataframe(filtered_data)

# Add a video (you can use a YouTube link or local file)
st.video("https://youtu.be/eyAAUGhvZu8?si=7f929728B6L-c00c") 
