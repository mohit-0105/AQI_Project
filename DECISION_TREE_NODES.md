# Decision Tree — Example Decision Nodes

This file illustrates how a single Decision Tree (from the Random Forest) splits the data to predict AQI. Each node represents a decision based on a pollutant value. The tree is trained to minimize prediction error at each split.

---

## Example: Top Levels of a Decision Tree for AQI Prediction

```
Node 0: Is PM2.5 ≤ 72.5?
├── Yes:
│   Node 1: Is CO ≤ 1.2?
│   ├── Yes:
│   │   Node 3: Is NO2 ≤ 18.5?
│   │   ├── Yes: Predict AQI ≈ 45 (Good)
│   │   └── No:  Predict AQI ≈ 85 (Satisfactory)
│   └── No:
│       Node 4: Is PM10 ≤ 60?
│       ├── Yes: Predict AQI ≈ 110 (Moderate)
│       └── No:  Predict AQI ≈ 150 (Moderate)
└── No:
    Node 2: Is CO ≤ 3.8?
    ├── Yes:
    │   Node 5: Is PM2.5 ≤ 180?
    │   ├── Yes: Predict AQI ≈ 220 (Poor)
    │   └── No:  Predict AQI ≈ 320 (Very Poor)
    └── No:
        Node 6: Is PM2.5 ≤ 320?
        ├── Yes: Predict AQI ≈ 410 (Severe)
        └── No:  Predict AQI ≈ 480 (Hazardous)
```

---

## Explanation
- **Each node** checks a pollutant value (e.g., "Is PM2.5 ≤ 72.5?").
- **Left branch** is taken if the answer is Yes; **right branch** if No.
- **Leaf nodes** (endpoints) output a predicted AQI value (the average AQI of all samples reaching that leaf).
- **Splits** are chosen to best separate the data and minimize prediction error at each step.
- **Random Forest** builds 100 such trees, each with different splits and thresholds, and averages their predictions for the final result.

---

## Why These Features?
- The tree prioritizes features with the highest importance (PM2.5, CO, PM10, NO2) at the top splits.
- Lower-importance features (e.g., Benzene, NH3) may appear deeper in the tree or not at all in a given tree.

---

## Note
- This is a simplified, human-readable example. Actual trees may be much deeper and use more features.
- You can visualize a real tree using `sklearn.tree.export_text()` or `plot_tree()` in Python.
