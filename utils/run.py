from datetime import datetime

import pandas as pd

# Get today's date in 'YYYY-MM-DD' format
today = datetime.today().strftime('%Y-%m-%d')
print(f"Today's date: {today}")

# Load the existing Excel file
try:
    df = pd.read_excel("~/Desktop/复盘表.xlsx")
    # Ensure '日期' column is in datetime format for proper comparison
    df['日期'] = pd.to_datetime(df['日期']).dt.strftime('%Y-%m-%d')
    last_date_str = df["日期"].iloc[-1]
    print(f"Last date in 复盘表.xlsx: {last_date_str}")
except FileNotFoundError:
    print("复盘表.xlsx not found. Creating a new one.")
    df = pd.DataFrame() # Create an empty DataFrame if the file doesn't exist
    last_date_str = "1900-01-01" # Set a very old date if the file is new

# Load the new CSV data
df2 = pd.read_csv("/data/project/2025/sentiment/sector_sts.csv")
# Ensure '日期' column in df2 is also in 'YYYY-MM-DD' format for consistent comparison
df2['日期'] = pd.to_datetime(df2['日期']).dt.strftime('%Y-%m-%d')

# Filter df2 for data from last_date_str to today
# Convert string dates back to datetime objects for proper comparison
last_date_dt = datetime.strptime(last_date_str, '%Y-%m-%d')
today_dt = datetime.strptime(today, '%Y-%m-%d')

# Filter for dates strictly greater than last_date_dt if you don't want to duplicate the last day,
# or greater than or equal if you want to include data for the last_date_dt from the CSV.
# Here, I'm filtering for dates strictly after last_date_dt to avoid potential duplicates
# if the last date in the Excel file already contains the full data for that day from the CSV.
# If you want to overwrite or update the last day's data from CSV, use `>= last_date_dt` and then drop duplicates.
new_data_to_add = df2[(df2["日期"] > last_date_str) & (df2["日期"] <= today)]

# Concatenate the original DataFrame with the new data
final_df = pd.concat([df, new_data_to_add], ignore_index=True)

# Remove any potential duplicate rows based on all columns, keeping the last occurrence (which would be from the new data)
final_df.drop_duplicates(inplace=True)

# Save the updated DataFrame back to Excel
final_df.to_excel("~/Desktop/复盘表.xlsx", index=False)
print("Data successfully merged and saved to 复盘表.xlsx!")