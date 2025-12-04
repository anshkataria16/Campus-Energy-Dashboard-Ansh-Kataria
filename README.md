# Campus-Energy-Dashboard-Ansh-Kataria
#Objective

The purpose of this project is to help the campus facilities team identify energy-saving opportunities by analyzing electricity consumption data from multiple buildings.
The project aims to:

* Combine meter data from multiple buildings.
* Clean and validate raw datasets.
* Perform daily and weekly energy analysis.
* Generate visual dashboards for decision-making.
* Produce a summary report highlighting patterns and anomalies.

#Dataset Source
The electricity usage data was stored as multiple `.csv` files inside a `/data/` directory.
Each file represented **one building’s hourly meter readings**, containing:

| Column      | Description                                    |
| `timestamp` | Date and hour of energy measurement            |
| `kwh`       | Electricity consumed during that hour          |
| `building`  | Building name (added automatically if missing) |

#Methodology

#1. Data Ingestion

* Used `os.listdir()` to detect all CSV files inside the `data/` folder.
* Loaded each file using `pandas.read_csv()`.
* Added missing metadata (building name).
* Handled corrupt/missing files using try–except.

#2. Data Cleaning

* Converted timestamps to `datetime` format.
* Sorted all data chronologically.
* Combined all building files into a single clean dataset.
* Exported final dataset as `cleaned_energy_data.csv`.

#3. Aggregation & Analysis

Performed multiple levels of statistical analysis:

* **Daily totals:** `resample("D").sum()`
* **Weekly totals:** `resample("W").sum()`
* **Building-wise summary:** mean, min, max, and total energy usage

These results were also exported to `building_summary.csv`.

### **4. Object-Oriented Approach**

Implemented three classes:

* **Building** → stores readings, calculates totals
* **MeterReading** → represents a single reading
* **BuildingManager** → manages all buildings and their data

This design makes the project scalable and readable.

###5. Executive Summary

Generated a `summary.txt` file containing:

* Total campus consumption
* Highest-consuming building
* Peak load time
* Overall trends and observations

#Key Insights

# ⭐ Total Energy Consumption

* The combined dataset shows significant variation in kWh usage across buildings.

# ⭐ Highest Consuming Building

* One building consistently records higher kWh values, indicating:

  * Higher occupancy
  * More equipment usage
  * Possible inefficiencies

# ⭐ Peak Load Times

* Peak loads typically occur:

  * Between **10 AM – 4 PM**
  * During working/lecture hours

# ⭐ Daily & Weekly Trends

* Weekly charts reveal a stable pattern after aggregating daily noise.
* Daily lines show fluctuations but follow a predictable daytime rise.

# ⭐ Opportunities for Energy Saving

* Buildings with unusually high consumption should undergo:

  * Equipment checks
  * HVAC optimization
  * Occupancy-based scheduling

#Generated Output Files

| File                      | Description                  |
| ------------------------- | ---------------------------- |
| `cleaned_energy_data.csv` | Combined and cleaned dataset |
| `building_summary.csv`    | Stats per building           |
| `summary.txt`             | Executive summary report     |

#Conclusion

This project demonstrates how data analytics can help campuses identify energy-saving opportunities. The pipeline—from ingestion to dashboard creation—provides an automated, scalable way to understand energy usage patterns and support smarter decision-making.
