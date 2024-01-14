import pandas as pd
# Print the number of 1s in the circle column in the csv
# Load the CSV
df = pd.read_csv('combined_brain_button_data.csv')
# Print the number of 1s in the circle column
print(df['Circle'].sum())


if __name__ == '__main__':
    print(df.head())