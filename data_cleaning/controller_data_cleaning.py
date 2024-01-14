# import pandas as pd
#
# # Load the first CSV
# df1 = pd.read_csv('../data_for_cleaning/controller_v1/button_log.csv', header=None, names=['Button', 'Code', 'Action', 'Timestamp'])
# df1['Timestamp'] = pd.to_datetime(df1['Timestamp'])
#
# # Load the second CSV
# df2 = pd.read_csv('../data_for_cleaning/controller_v1/brain_data.csv', header=None, names=['data', 'Timestamp'], parse_dates=['Timestamp'])
#
# # Add columns for each button in df2 with all zeros
# buttons = df1['Button'].unique()
# for button in buttons:
#     df2[button] = 0
#
# # Update df2 based on df1
# for button in buttons:
#     pressed_times = df1[(df1['Button'] == button) & (df1['Action'] == 'Pressed')]['Timestamp']
#     released_times = df1[(df1['Button'] == button) & (df1['Action'] == 'Released')]['Timestamp']
#
#     for pressed_time, released_time in zip(pressed_times, released_times):
#         df2.loc[(df2['Timestamp'] >= pressed_time) & (df2['Timestamp'] <= released_time), button] = 1
#
# # Save the updated data to a new CSV file
# df2.to_csv('new_second_csv.csv', index=False)
#
# if __name__ == '__main__':
#     print(df1.head())
#     print(df2.head())

import pandas as pd
import json


# Function to unpack JSON data
def unpack_json(row):
    try:
        # Replace single quotes with double quotes for JSON parsing
        json_data = json.loads(row['data'].replace("'", "\""))
        channels = json_data['info']['channelNames']
        data = json_data['data']

        # Flatten the nested list structure and create a column for each data point
        unpacked_data = {}
        for i, channel in enumerate(channels):
            for j, value in enumerate(data[i]):
                column_name = f"{channel}_{j}"
                unpacked_data[column_name] = value
        return pd.Series(unpacked_data)
    except (TypeError, json.JSONDecodeError) as e:
        print(f"Error unpacking JSON data at row {row.name}: {e}")
        return pd.Series({})


# Load the button log data (first CSV)
df1 = pd.read_csv('../data_for_cleaning/controller_v1/button_log.csv', header=None,
                  names=['Button', 'Code', 'Action', 'Timestamp'])
df1['Timestamp'] = pd.to_datetime(df1['Timestamp'])

# Load the brain data (second CSV) and unpack it
df2 = pd.read_csv('../data_for_cleaning/controller_v1/brain_data.csv', header=None, names=['data', 'Timestamp'],
                  parse_dates=['Timestamp'])
df2 = df2.join(df2.apply(unpack_json, axis=1))

# Add columns for each button with all zeros
buttons = df1['Button'].unique()
for button in buttons:
    df2[button] = 0

# Update df2 based on df1
for button in buttons:
    pressed_times = df1[(df1['Button'] == button) & (df1['Action'] == 'Pressed')]['Timestamp']
    released_times = df1[(df1['Button'] == button) & (df1['Action'] == 'Released')]['Timestamp']

    for pressed_time, released_time in zip(pressed_times, released_times):
        df2.loc[(df2['Timestamp'] >= pressed_time) & (df2['Timestamp'] <= released_time), button] = 1

# Save the updated data to a new CSV file
df2.to_csv('combined_brain_button_data.csv', index=False)

if __name__ == '__main__':
    print(df1.head())
    print(df2.head())
