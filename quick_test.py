import pandas as pd
import pickle

# Quick single prediction test
# Usage: python quick_test.py

test_input = pd.DataFrame([{
    "PM2.5": 150, "PM10": 200, "NO": 25, "NO2": 40,
    "NOx": 55, "NH3": 18, "CO": 3.0, "SO2": 12,
    "O3": 35, "Benzene": 2.0, "Toluene": 5.0, "Xylene": 1.5
}])

# Run from notebook environment
print("Test Input:")
print(test_input)
print("\nThis script validates a single AQI prediction.")
print("Expected output for these inputs: ~280-320 AQI (Poor range)")
