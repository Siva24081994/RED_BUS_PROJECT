import streamlit as st
import mysql.connector
import pandas as pd

# MySQL connection setup
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Replace with your MySQL root password
        database="RED_BUS"
    )

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

# Sidebar filters (route name first, then bus type, then bus name)
def sidebar_filters():
    st.sidebar.header("Filter Options")

    # Route Name Filter (first)
    routes = load_data("SELECT DISTINCT route_name FROM RED_BUS_ROUTES")
    route_filter = st.sidebar.multiselect("Route Name", routes['route_name'])

    # Bus Type Filter (second)
    bus_types = load_data("SELECT DISTINCT bustype FROM RED_BUS_ROUTES")
    bus_type_filter = st.sidebar.multiselect("Bus Type", bus_types['bustype'])

    # Bus Name Filter (third)
    bus_names = load_data("SELECT DISTINCT busname FROM RED_BUS_ROUTES")
    bus_name_filter = st.sidebar.multiselect("Bus Name", bus_names['busname'])

    # Price Range Filter
    price_min, price_max = load_data("SELECT MIN(price), MAX(price) FROM RED_BUS_ROUTES").iloc[0]
    price_range_filter = st.sidebar.slider("Price Range", float(price_min), float(price_max), (float(price_min), float(price_max)))

    # Star Rating Filter
    star_rating_filter = st.sidebar.slider("Minimum Star Rating", 0.0, 5.0, 0.0)

    # Seat Availability Filter
    seat_availability_filter = st.sidebar.slider("Minimum Seats Available", 0, 50, 0)

    return route_filter, bus_type_filter, bus_name_filter, price_range_filter, star_rating_filter, seat_availability_filter

# Build the SQL query based on user inputs
def filter_data(route, bus_type, bus_name, price_range, star_rating, seat_availability):
    # Start with a base query
    query = "SELECT * FROM RED_BUS_ROUTES WHERE 1=1"
    params = []

    # Route filter (first)
    if route:
        query += " AND route_name IN (%s)" % ','.join(['%s'] * len(route))
        params.extend(route)

    # Bus type filter (second)
    if bus_type:
        query += " AND bustype IN (%s)" % ','.join(['%s'] * len(bus_type))
        params.extend(bus_type)

    # Bus name filter (third)
    if bus_name:
        query += " AND busname IN (%s)" % ','.join(['%s'] * len(bus_name))
        params.extend(bus_name)

    # Price range filter
    query += " AND price BETWEEN %s AND %s"
    params.extend(price_range)

    # Star rating filter
    if star_rating > 0.0:
        query += " AND star_rating >= %s"
        params.append(star_rating)

    # Seat availability filter
    if seat_availability > 0:
        query += " AND seats_available >= %s"
        params.append(seat_availability)

    return query, params

# Main Streamlit application
def main():
    st.title("Redbus Data Analysis and Filtering")

    # Sidebar filters with route name first
    route, bus_type, bus_name, price_range, star_rating, seat_availability = sidebar_filters()

    # Filter data based on user input
    filter_query, params = filter_data(route, bus_type, bus_name, price_range, star_rating, seat_availability)
    filtered_data = load_data(filter_query, params)

    # Display filtered data
    st.write("### Filtered Bus Data")
    st.dataframe(filtered_data)

if __name__ == "__main__":
    main()
