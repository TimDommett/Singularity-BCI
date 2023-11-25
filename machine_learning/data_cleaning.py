import pandas as pd
import json

# Load the raw data
brain_data_path = '../data_backups/brain_data.csv'  # Replace with the actual path to your brain data file
brain_data = pd.read_csv(brain_data_path, header=None)

# Define a default JSON object to fill NaN values
default_json_obj = json.dumps({"data": [], "info": {"channelNames": [], "notchFrequency": None, "samplingRate": None, "startTime": None}})

# Fill NaN values with the default JSON object
brain_data[0].fillna(default_json_obj, inplace=True)

# Replace single quotes with double quotes and then deserialize the JSON data
brain_data[0] = brain_data[0].str.replace("'", '"').apply(json.loads)

# Create separate columns for the different pieces of data
brain_data['EEG_data'] = [x['data'] for x in brain_data[0]]
brain_data['channel_names'] = [x['info']['channelNames'] for x in brain_data[0]]
brain_data['notch_frequency'] = [x['info']['notchFrequency'] for x in brain_data[0]]
brain_data['sampling_rate'] = [x['info']['samplingRate'] for x in brain_data[0]]
brain_data['start_time'] = [x['info']['startTime'] for x in brain_data[0]]

# Rename the columns for better understanding and convert the timestamp columns to datetime objects
brain_data.rename(columns={1: 'timestamp'}, inplace=True)
brain_data['timestamp'] = pd.to_datetime(brain_data['timestamp'])

# Set the timestamp columns as the indices of both dataframes
brain_data.set_index('timestamp', inplace=True)

# Drop the original column that contained the serialized JSON data
brain_data.drop(columns=[0], inplace=True)

# Save the cleaned data to a new CSV file
cleaned_data_path = '../data_backups/cleaned_brain_data.csv'  # Replace with the path where you want to save the cleaned data
brain_data.to_csv(cleaned_data_path)

if __name__ == '__main__':
    print(brain_data.info())
