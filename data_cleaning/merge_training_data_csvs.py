# import pandas as pd
# import json
#
#
# # Function to read CSV file
# def read_csv_file(file_path):
#     return pd.read_csv(file_path)
#
#
# # Function to unpack JSON data
# def unpack_json(row, sampling_rate=256):
#     if not isinstance(row['Data'], str):
#         print(f"Skipping non-string data at row {row.name}")
#         return pd.Series({})
#
#     try:
#         json_data = json.loads(row['Data'].replace("'", "\""))
#         channels = json_data['info']['channelNames']
#         data = json_data['data']
#
#         # Calculate time interval in milliseconds
#         time_interval_ms = 1000 / sampling_rate  # Convert to milliseconds
#
#         unpacked_data = {}
#         for i, channel in enumerate(channels):
#             for j, value in enumerate(data[i]):
#                 # Create a column name for each data point
#                 column_name = f"{channel}_{int(j * time_interval_ms)}ms"
#                 unpacked_data[column_name] = value
#         return pd.Series(unpacked_data)
#     except (TypeError, json.JSONDecodeError) as e:
#         print(f"Error unpacking JSON data at row {row.name}: {e}")
#         return pd.Series({})
#
#
# # Read the CSVs
# brain_data = read_csv_file('brain_data_cleaned.csv')
# keystroke_data = read_csv_file('keystrokes_log.csv')
#
# # Convert time columns to datetime
# brain_data['time'] = pd.to_datetime(brain_data['Time'])
# keystroke_data['time'] = pd.to_datetime(keystroke_data['time'])
#
# # Unpack the JSON data
# brain_data = brain_data.join(brain_data.apply(unpack_json, axis=1))
#
# # Drop the original data column
# brain_data.drop(columns=['Data'], inplace=True)
#
# # Merge the dataframes based on the closest timestamps
# merged_data = pd.merge_asof(keystroke_data.sort_values('time'), brain_data.sort_values('time'), on='time')
#
# # Save the result to a new CSV
# merged_data.to_csv('merged_data_2.csv', index=False)
#
# if __name__ == '__main__':
#     print("Merged data saved to merged_data_2.csv")
import pandas as pd
import json


# Function to read CSV file
def read_csv_file(file_path):
    return pd.read_csv(file_path)


# Function to unpack JSON data
def unpack_json(row, sampling_rate=256):
    if not isinstance(row['Data'], str):
        print(f"Skipping non-string data at row {row.name}")
        return pd.Series({})

    try:
        json_data = json.loads(row['Data'].replace("'", "\""))
        channels = json_data['info']['channelNames']
        data = json_data['data']

        # Calculate time interval in milliseconds
        time_interval_ms = 1000 / sampling_rate  # Convert to milliseconds

        unpacked_data = {}
        for i, channel in enumerate(channels):
            for j, value in enumerate(data[i]):
                # Create a column name for each data point
                column_name = f"{channel}_{int(j * time_interval_ms)}ms"
                unpacked_data[column_name] = value
        return pd.Series(unpacked_data)
    except (TypeError, json.JSONDecodeError) as e:
        print(f"Error unpacking JSON data at row {row.name}: {e}")
        return pd.Series({})


# Read the CSVs
brain_data = read_csv_file('brain_data_cleaned.csv')
keystroke_data = read_csv_file('keystrokes_log.csv')

# Convert time columns to datetime
brain_data['time'] = pd.to_datetime(brain_data['Time'])
keystroke_data['time'] = pd.to_datetime(keystroke_data['time'])

# Unpack the JSON data
brain_data = brain_data.join(brain_data.apply(unpack_json, axis=1))

# Drop the original data column
brain_data.drop(columns=['Data'], inplace=True)

# Initialize columns for keystrokes in brain_data with 'None'
for col in keystroke_data.columns.drop('time'):
    brain_data[col] = 'None'

# Define a threshold for time difference (e.g., 1 second)
time_threshold = pd.Timedelta(seconds=1)

# Assign keystrokes to the closest brain data within the threshold
used_keystrokes = set()
for idx, keystroke_row in keystroke_data.iterrows():
    # Find the closest time in brain_data
    closest_brain_data = brain_data.iloc[(brain_data['time'] - keystroke_row['time']).abs().argsort()[:1]]

    # Check if the closest brain data is within the threshold and not already used
    if not closest_brain_data.empty:
        closest_idx = closest_brain_data.index[0]
        if closest_idx not in used_keystrokes and abs(
                closest_brain_data['time'].iloc[0] - keystroke_row['time']) <= time_threshold:
            for col in keystroke_data.columns.drop('time'):
                brain_data.at[closest_idx, col] = keystroke_row[col]
            used_keystrokes.add(closest_idx)

# Save the result to a new CSV
brain_data.to_csv('merged_data_7.csv', index=False)

if __name__ == '__main__':
    print("Merged data saved to merged_data_7csv")
