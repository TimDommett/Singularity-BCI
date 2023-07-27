import pandas as pd
import json
import ast
import numpy as np

# Load the keystroke data
keystrokes = pd.read_csv('../../test_data/keystrokes_log_batch_1.csv', names=['Keystroke', 'Timestamp'])
keystrokes['Timestamp'] = pd.to_datetime(keystrokes['Timestamp'])

# Load the EEG data
eeg = pd.read_csv('../../test_data/brain_data.csv', names=['Data', 'Timestamp'])
eeg['Timestamp'] = pd.to_datetime(eeg['Timestamp'])

# We will convert the JSON data into columns
def convert_json(row):
    json_data = json.loads(row['Data'])
    for key, value in json_data.items():
        if isinstance(value, dict):
            for inner_key, inner_value in value.items():
                row[f'Data_{key}_{inner_key}'] = inner_value
        else:
            row[f'Data_{key}'] = value
    return row


def unpack_row(row):
    # Convert the data string into a Python dictionary
    data_dict = ast.literal_eval(row)

    # Create an empty DataFrame
    df = pd.DataFrame()

    # Iterate over the data lists
    for i, data_list in enumerate(data_dict['data']):
        # Create a new DataFrame from the data list
        df_temp = pd.DataFrame(data_list, columns=[f'data_{i}'])

        # Concatenate the new DataFrame to the main DataFrame
        df = pd.concat([df, df_temp], axis=1)

    # Add the timestamp as a new column in the DataFrame
    df['timestamp'] = data_dict['timestamp']

    return df


# def process_eeg_data(file_path):
#     # Load the csv file
#     df = pd.read_csv(file_path)
#
#     # Convert the string representation of a dictionary into an actual dictionary
#     df['data_dict'] = df.iloc[:, 0].apply(ast.literal_eval)
#
#     # Create new columns from the dictionary
#     df = df.join(pd.json_normalize(df['data_dict']))
#
#     # Drop the original column
#     df = df.drop(columns=[df.columns[0], 'data_dict'])
#
#     # Unpack the lists in the 'data' column into a new dataframe
#     data_df = pd.DataFrame(df['data'].to_list(), columns=df['info.channelNames'][0])
#
#     # Concatenate the new dataframe with the original dataframe
#     df = pd.concat([df, data_df], axis=1)
#
#     # Drop the original 'data' column
#     df = df.drop(columns='data')
#
#     # Define a function to expand a list into multiple columns and add a suffix to the column names
#     def expand_list(df, list_column, prefix):
#         # Expand the list_column into a DataFrame and add a prefix to the column names
#         expanded = pd.DataFrame(df[list_column].to_list()).add_prefix(f'{prefix}_')
#
#         # Concatenate the expanded DataFrame with the original DataFrame
#         df = pd.concat([df, expanded], axis=1)
#
#         # Drop the original list_column
#         df = df.drop(columns=list_column)
#
#         return df
#
#     # Apply the function to each EEG channel column
#     for channel in df['info.channelNames'][0]:
#         df = expand_list(df, channel, channel)
#
#     return df

def process_eeg_data(file_path):
    # Load the csv file
    df = pd.read_csv(file_path)

    # Drop rows with missing values
    df = df.dropna()

    # Convert the string representation of a dictionary into an actual dictionary
    # Ignore rows where this operation fails
    try:
        df['data_dict'] = df.iloc[:, 0].apply(ast.literal_eval)
    except ValueError:
        return pd.DataFrame()

    # Create new columns from the dictionary
    # Ignore rows where this operation fails
    try:
        df = df.join(pd.json_normalize(df['data_dict']))
    except ValueError:
        return pd.DataFrame()

    # Drop the original column
    df = df.drop(columns=[df.columns[0], 'data_dict'])

    # Unpack the lists in the 'data' column into a new dataframe
    # Ignore rows where this operation fails
    try:
        data_df = pd.DataFrame(df['data'].to_list(), columns=df['info.channelNames'][0])
    except ValueError:
        return pd.DataFrame()

    # Concatenate the new dataframe with the original dataframe
    df = pd.concat([df, data_df], axis=1)

    # Drop the original 'data' column
    df = df.drop(columns='data')

    # Define a function to expand a list into multiple columns and add a suffix to the column names
    def expand_list(df, list_column, prefix):
        # Expand the list_column into a DataFrame and add a prefix to the column names
        expanded = pd.DataFrame(df[list_column].to_list()).add_prefix(f'{prefix}_')

        # Concatenate the expanded DataFrame with the original DataFrame
        df = pd.concat([df, expanded], axis=1)

        # Drop the original list_column
        df = df.drop(columns=list_column)

        return df

    # Apply the function to each EEG channel column
    for channel in df['info.channelNames'][0]:
        df = expand_list(df, channel, channel)

    # Change first column name to 'Timestamp'
    df = df.rename(columns={df.columns[0]: 'Timestamp'})

    return df


processed_eeg_data = process_eeg_data('../../test_data/brain_data_batch_1.csv')

# Update Timestamp column data type to datetime
processed_eeg_data['Timestamp'] = pd.to_datetime(processed_eeg_data['Timestamp'])

# Unpack each row and concatenate them into a new dataframe
# new_df = pd.concat(eeg['Data'].apply(unpack_row).tolist(), ignore_index=True)
#
# eeg = eeg.apply(convert_json, axis=1)
# eeg = eeg.drop(columns=['Data'])

# Merge the two dataframes
combined = pd.merge_asof(keystrokes, processed_eeg_data, on='Timestamp')



# Save to a new CSV
combined.to_csv('combined.csv', index=False)

if __name__ == '__main__':
    print(combined.head())

