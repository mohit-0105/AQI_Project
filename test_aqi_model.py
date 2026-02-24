import pandas as pd
import numpy as np

# Test cases for AQI prediction model
# These scenarios validate model across pollution spectrum

test_cases = [
    {"name": "Heavy Pollution - Delhi Winter",
     "PM2.5": 250, "PM10": 300, "NO": 40, "NO2": 60, "NOx": 80,
     "NH3": 20, "CO": 5.0, "SO2": 25, "O3": 40,
     "Benzene": 3.0, "Toluene": 5.0, "Xylene": 2.0,
     "expected_category": "Very Poor"},

    {"name": "Clean Day - Hill Station",
     "PM2.5": 12, "PM10": 25, "NO": 3, "NO2": 8, "NOx": 10,
     "NH3": 5, "CO": 0.3, "SO2": 3, "O3": 20,
     "Benzene": 0.5, "Toluene": 1.0, "Xylene": 0.3,
     "expected_category": "Good"},

    {"name": "Moderate Urban Day",
     "PM2.5": 80, "PM10": 100, "NO": 15, "NO2": 25, "NOx": 35,
     "NH3": 15, "CO": 1.5, "SO2": 10, "O3": 30,
     "Benzene": 2.0, "Toluene": 3.0, "Xylene": 1.0,
     "expected_category": "Moderate"},

    {"name": "Extreme Industrial",
     "PM2.5": 400, "PM10": 500, "NO": 80, "NO2": 100, "NOx": 150,
     "NH3": 40, "CO": 10.0, "SO2": 50, "O3": 60,
     "Benzene": 6.0, "Toluene": 10.0, "Xylene": 4.0,
     "expected_category": "Hazardous"},

    {"name": "Near-Clean Rural",
     "PM2.5": 5, "PM10": 10, "NO": 1, "NO2": 2, "NOx": 3,
     "NH3": 2, "CO": 0.1, "SO2": 1, "O3": 15,
     "Benzene": 0.1, "Toluene": 0.2, "Xylene": 0.1,
     "expected_category": "Good"},
]

print("=== AQI MODEL TEST CASES ===\n")
for tc in test_cases:
    print(f"Scenario : {tc['name']}")
    print(f"PM2.5    : {tc['PM2.5']} µg/m³")
    print(f"CO       : {tc['CO']} ppm")
    print(f"Expected : {tc['expected_category']}")
    print("-" * 40)
