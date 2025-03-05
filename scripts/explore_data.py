import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re

# Set display options
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
plt.style.use('seaborn-v0_8-whitegrid')

# Function to clean numeric columns (remove currency symbols, commas, etc.)
def clean_numeric(val):
    if isinstance(val, str):
        # Remove currency symbols, commas, percentage signs
        val = re.sub(r'[$,€£%]', '', val)
        # Convert to float
        try:
            return float(val)
        except:
            return val
    return val

# Function to load a CSV file and convert numeric columns
def load_csv(file_path):
    df = pd.read_csv(file_path)
    
    # Clean column names
    df.columns = [col.strip() for col in df.columns]
    
    # Try to convert numeric columns
    numeric_cols = ['Cost', 'Clicks', 'Impressions', 'Conversions', 'CTR', 'Avg. CPC', 'Conv. value']
    for col in df.columns:
        if any(metric in col for metric in numeric_cols):
            df[col] = df[col].apply(clean_numeric)
    
    return df

# Function to show basic CSV file information
def explore_csv(file_path):
    file_name = os.path.basename(file_path)
    print(f"\n{'='*50}")
    print(f"File: {file_name}")
    print(f"{'='*50}")
    
    df = load_csv(file_path)
    
    print(f"Shape: {df.shape}")
    print("\nColumn names:")
    for col in df.columns:
        print(f"- {col}")
    
    print("\nSample data (first 5 rows):")
    print(df.head())
    
    # Basic stats for numeric columns
    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 0:
        print("\nNumeric columns summary:")
        print(df[numeric_cols].describe())
    
    return df

# Main exploration function
def explore_google_ads_data(data_dir):
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    print(f"Found {len(csv_files)} CSV files in {data_dir}")
    
    # Dictionary to store dataframes
    dataframes = {}
    
    # Explore each file
    for file in csv_files:
        file_path = os.path.join(data_dir, file)
        df = explore_csv(file_path)
        dataframes[file] = df
    
    return dataframes

# Usage - update with your data directory
data_dir = "data"  # Change this to your data directory if different
dataframes = explore_google_ads_data(data_dir)

# Quick Campaign Analysis
if 'Campaigns.csv' in dataframes:
    campaigns_df = dataframes['Campaigns.csv']
    
    # Convert Cost and Clicks to numeric if they aren't already
    for col in ['Cost', 'Clicks']:
        if col in campaigns_df.columns:
            campaigns_df[col] = pd.to_numeric(campaigns_df[col], errors='coerce')
    
    # Basic campaign performance visualization
    if all(col in campaigns_df.columns for col in ['Campaign Name', 'Cost']):
        # Sort by cost and get top 5
        top_campaigns = campaigns_df.sort_values('Cost', ascending=False).head(5)
        
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Cost', y='Campaign Name', data=top_campaigns)
        plt.title('Top 5 Campaigns by Cost')
        plt.tight_layout()
        plt.show()

# Quick Device Analysis
if 'Devices.csv' in dataframes:
    devices_df = dataframes['Devices.csv']
    
    # Convert Cost to numeric if it isn't already
    if 'Cost' in devices_df.columns:
        devices_df['Cost'] = pd.to_numeric(devices_df['Cost'], errors='coerce')
    
    # Device performance visualization
    if all(col in devices_df.columns for col in ['Device', 'Cost']):
        plt.figure(figsize=(8, 5))
        sns.barplot(x='Device', y='Cost', data=devices_df)
        plt.title('Cost by Device')
        plt.tight_layout()
        plt.show()

# Time Series Analysis
if 'Time_series.csv' in dataframes:
    time_df = dataframes['Time_series.csv']
    
    # Convert columns to numeric if they aren't already
    for col in ['Clicks', 'Impressions', 'Cost']:
        if col in time_df.columns:
            time_df[col] = pd.to_numeric(time_df[col], errors='coerce')
    
    # Convert Week to datetime if possible
    if 'Week' in time_df.columns:
        try:
            time_df['Week'] = pd.to_datetime(time_df['Week'])
            time_df = time_df.sort_values('Week')
        except:
            # If datetime conversion fails, just use the Week column as is
            pass
    
    # Time series visualization
    if 'Week' in time_df.columns and 'Cost' in time_df.columns:
        plt.figure(figsize=(12, 6))
        plt.plot(time_df['Week'], time_df['Cost'], marker='o', linestyle='-')
        plt.title('Weekly Ad Spend Over Time')
        plt.xlabel('Week')
        plt.ylabel('Cost')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

print("\nExploration complete! This initial analysis gives you a basic understanding of your data.")
print("Next steps could include:")
print("1. More detailed campaign performance analysis")
print("2. Keyword performance analysis")
print("3. Search query analysis")
print("4. Day and hour optimization")
print("5. Developing budget optimization recommendations")