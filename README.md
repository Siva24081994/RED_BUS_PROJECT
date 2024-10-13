# RED_BUS_PROJECT
Redbus Data Scraping and Filtering with Streamlit Application

Project Overview
This project automates the web scraping of bus data from the Redbus website, stores the data in a structured SQL database, and builds an interactive application using Streamlit. Users can filter and explore bus routes, schedules, prices, seat availability, and more. This project leverages Python, Selenium, SQL, and Streamlit to enhance data-driven decision-making in the transportation domain.

Table of Contents
Skills Takeaway
Domain
Problem Statement
Business Use Cases
Approach
Database Schema
SQL Script to Create the Database and Table
Python Code Overview
Results

By working on this project, you will develop the following skills:

Web Scraping using Selenium
Python Programming
SQL Database Interaction
Streamlit for building interactive web applications
Data Filtering and Analysis

Domain: Transportation
The transportation industry can benefit from automated data scraping, analysis, and visualization to improve operational efficiency and strategic planning.

Problem Statement
The Redbus Data Scraping and Filtering with Streamlit Application aims to automate the extraction, storage, and analysis of bus travel data from the Redbus website. The application allows users to filter and analyze data, providing valuable insights for businesses and travelers.

Challenges Solved:
Automating data extraction with Selenium.
Storing scraped data in an SQL database.
Allowing users to interactively filter and analyze data via Streamlit.
Business Use Cases
This solution can be applied in various business scenarios:

Travel Aggregators: Providing real-time bus schedules and seat availability for customers.
Market Analysis: Understanding travel patterns for market research.
Customer Service: Offering personalized travel recommendations based on data insights.
Competitor Analysis: Comparing pricing and service levels with competitors.
Approach
Data Scraping: Selenium is used to scrape Redbus data, including routes, schedules, prices, and seat availability.
Data Storage: The scraped data is stored in an SQL database named Red_bus_project, in the table redbus_routes.
Streamlit Application: A Streamlit application is developed to visualize and filter the scraped data with filters for route, bus type, price range, star rating, and seat availability.
Data Analysis: The application retrieves data using SQL queries based on user inputs, allowing for dynamic filtering and data exploration.

Database Schema

Database Name: Red_bus_project
Table Name: redbus_routes

The redbus_routes table stores all the bus details scraped from Redbus. The table schema is as follows:

Column Name	Data Type	Description
id	INT	Primary Key (Auto-increment)
route_name	TEXT	The name of the bus route
route_link	TEXT	URL link for route details
busname	TEXT	The name of the bus
bustype	TEXT	The type of bus (Sleeper/Seater/AC/Non-AC)
departing_time	TIME	The time the bus departs
duration	TEXT	Duration of the journey
reaching_time	TIME	The time the bus reaches the destination
star_rating	FLOAT	The star rating given by passengers
price	DECIMAL	The ticket price
seats_available	INT	The number of seats available

SQL Script to Create the Database and Table:

CREATE DATABASE IF NOT EXISTS Red_bus_project;

USE Red_bus_project;

CREATE TABLE IF NOT EXISTS redbus_routes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    route_name TEXT NOT NULL,
    route_link TEXT,
    busname TEXT NOT NULL,
    bustype TEXT NOT NULL,
    departing_time TIME,
    duration TEXT NOT NULL,
    reaching_time TIME,
    star_rating FLOAT,
    price DECIMAL(10, 2) NOT NULL,
    seats_available INT NOT NULL
);
Python Code Overview

Data Scraping with Selenium
The following code demonstrates scraping data using Selenium:

python

from selenium import webdriver
from selenium.webdriver.common.by import By

# Set up WebDriver (ChromeDriver in this case)
driver = webdriver.Chrome()

# Open Redbus Website
driver.get("https://www.redbus.in/")

# Code to navigate and scrape relevant data from the website
# ...

# Close the browser
driver.quit()
This scraped data includes:

Route name and link
Bus name, type, and availability
Departing and reaching time
Star rating and price

SQL Database Interaction
After scraping the data, it is stored in the redbus_routes table in the Red_bus_project database:

python
import mysql.connector

# Establish connection to MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="Red_bus_project"
)

# SQL Insert Query
insert_query = """ 
INSERT INTO redbus_routes(route_name, route_link, busname, bustype, departing_time, duration, reaching_time, star_rating, price, seats_available) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
"""

# Example of inserting data
mycursor = mydb.cursor()
mycursor.execute(insert_query, (route_name, route_link, bus_name, bus_type, depart_time, duration, reach_time, star_rating, price, seats_available))
mydb.commit()

# Close connection
mycursor.close()
mydb.close()

Streamlit Application
The Streamlit app allows users to interactively filter the bus data based on parameters like route, price, and availability.

python
import streamlit as st
import pandas as pd
import mysql.connector

# Streamlit Filters and UI
route = st.selectbox("Select Route", ["Route 1", "Route 2", "Route 3"])
price_range = st.slider("Price Range", 100, 5000)

# Fetch filtered data from SQL database
def fetch_data(route, price_range):
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="Red_bus_project")
    query = f"SELECT * FROM redbus_routes WHERE route_name = '{route}' AND price <= {price_range}"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Display data
filtered_data = fetch_data(route, price_range)
st.write(filtered_data)
Results
The project aims to achieve the following:

Successfully scrape data from Redbus for at least 10 Government State Bus Transport routes.
Store the data in an SQL database.
Develop an interactive Streamlit application for users to filter and explore the bus data.
