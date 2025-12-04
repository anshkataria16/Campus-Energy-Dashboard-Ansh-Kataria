import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
class MeterReading:
    def __init__(self, timestamp, kwh):
        self.timestamp = timestamp
        self.kwh = kwh


class Building:
    def __init__(self, name):
        self.name = name
        self.meter_readings = []

    def add_reading(self, reading: MeterReading):
        self.meter_readings.append(reading)

    def calculate_total_consumption(self):
        return sum(r.kwh for r in self.meter_readings)

    def generate_report(self):
        total = self.calculate_total_consumption()
        return f"{self.name}: Total Consumption = {total} kWh"


class BuildingManager:
    def __init__(self):
        self.buildings = {}

    def add_building_data(self, name, df):
        if name not in self.buildings:
            self.buildings[name] = Building(name)

        for _, row in df.iterrows():
            reading = MeterReading(row["timestamp"], row["kwh"])
            self.buildings[name].add_reading(reading)

def load_all_data(data_folder="data"):
    combined_df = pd.DataFrame()

    if not os.path.exists(data_folder):
        print("Data folder does not exist!")
        return combined_df

    files = os.listdir(data_folder)
    csv_files = [f for f in files if f.endswith(".csv")]

    if not csv_files:
        print("No CSV files found in data folder!")
        return combined_df

    for file in csv_files:
        file_path = os.path.join(data_folder, file)

        try:
            temp = pd.read_csv(file_path)
            temp["timestamp"] = pd.to_datetime(temp["timestamp"])

            building_name = file.replace(".csv", "")
            temp["building"] = building_name

            combined_df = pd.concat([combined_df, temp], ignore_index=True)

        except Exception as e:
            print(f"Error reading file {file}: {e}")

    print("All CSV files loaded successfully.")
    return combined_df


def calculate_daily_totals(df):
    return df.resample("D", on="timestamp")["kwh"].sum()


def calculate_weekly_aggregates(df):
    return df.resample("W", on="timestamp")["kwh"].sum()


def building_wise_summary(df):
    return df.groupby("building")["kwh"].agg(["mean", "min", "max", "sum"])


def create_dashboard(df_daily, df_weekly, df):
    fig, axs = plt.subplots(3, 1, figsize=(10, 12))

    # 1. Daily trend line
    axs[0].plot(df_daily.index, df_daily.values)
    axs[0].set_title("Daily Electricity Consumption")
    axs[0].set_ylabel("kWh")

    # 2. Weekly bar chart
    axs[1].bar(df_weekly.index, df_weekly.values)
    axs[1].set_title("Weekly Electricity Consumption")
    axs[1].set_ylabel("kWh")

    # 3. Scatter plot (hourly points)
    axs[2].scatter(df["timestamp"], df["kwh"], s=10)
    axs[2].set_title("Hourly Consumption")
    axs[2].set_ylabel("kWh")
    axs[2].set_xlabel("Time")

    plt.tight_layout()
    plt.savefig("dashboard.png")
    plt.close()
    print("Dashboard saved as dashboard.png")



def generate_summary(df, building_summary):
    total_consumption = df["kwh"].sum()
    highest_building = building_summary["sum"].idxmax()
    peak_row = df.loc[df["kwh"].idxmax()]

    with open("summary.txt", "w") as f:
        f.write("CAMPUS ENERGY SUMMARY\n")
        f.write("------------------------------\n")
        f.write(f"Total Campus Consumption: {total_consumption} kWh\n")
        f.write(f"Highest Consuming Building: {highest_building}\n")
        f.write(f"Peak Load Time: {peak_row['timestamp']} ({peak_row['kwh']} kWh)\n")
        f.write("\nDaily & Weekly charts saved in dashboard.png\n")

    print("Summary written to summary.txt")


def main():

    df = load_all_data("data")

    if df.empty:
        print("No data to process!")
        return

    df = df.sort_values("timestamp")

    daily = calculate_daily_totals(df)
    weekly = calculate_weekly_aggregates(df)
    summary = building_wise_summary(df)

    df.to_csv("cleaned_energy_data.csv", index=False)
    summary.to_csv("building_summary.csv")
    print("Cleaned data exported.")

    create_dashboard(daily, weekly, df)
    generate_summary(df, summary)

    print("ALL TASKS COMPLETED SUCCESSFULLY.")


if __name__ == "__main__":
    main()
