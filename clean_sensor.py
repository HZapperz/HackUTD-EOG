import pandas as pd

# Function to check if a number has more than 2 decimal places
def clean_data_remove2plus_decimals(number):
    if not pd.isnull(number):
        number_str = str(number)
        if '.' in number_str:  # Check if there is a decimal point
            decimal_part = number_str.split('.')[1]
            return len(decimal_part) > 2
    return False

# Function to clean data that is outside the sensor's detection range
def clean_data_outside_range(value, min_val=300, max_val=10000):
    if not pd.isnull(value) and (value < min_val or value > max_val):
        return pd.NA
    return value

def clean_sensor_data(sensor_readings_df):
    # Apply the function to each cell in the DataFrame, replace with NaN if condition is met
    # Assuming the first column is 'index' and the second column is 'time'
    for column in sensor_readings_df.columns[2:]:  # Start from the third column
        if sensor_readings_df[column].dtype in ['float64', 'int64']:
            # Clean data outside the sensor's range
            sensor_readings_df[column] = sensor_readings_df[column].apply(clean_data_outside_range)
            # Remove data with more than 2 decimal places
            sensor_readings_df[column] = sensor_readings_df[column].apply(
                lambda x: x if not clean_data_remove2plus_decimals(x) else pd.NA
            )
    return sensor_readings_df

def average_sensor_data(cleaned_df):
    # Initialize averaged_columns as an empty dictionary
    averaged_columns = {}
    
    try:
        # Attempt to select 'index' and 'time' columns
        initial_cols_df = cleaned_df[['index', 'time']]
    except KeyError as e:
        # Handle the absence of 'index' by resetting the index to create the column
        print(f"Column not found in DataFrame: {e}")
        cleaned_df = cleaned_df.reset_index()  # This will create an 'index' column
        initial_cols_df = cleaned_df[['index', 'time']]

    # Extract the coordinates from the column headers and group columns by coordinates
    grouped_columns = {}
    for column in cleaned_df.columns[2:]:  # We skip 'index' and 'time' which are the first two columns
        coords = "_".join(column.split('_')[1:-1])
        if coords not in grouped_columns:
            grouped_columns[coords] = []
        grouped_columns[coords].append(column)

    # Iterate over the groups and average the columns if there is more than one
    for coords, columns in grouped_columns.items():
        if len(columns) == 1:
            averaged_columns[coords] = cleaned_df[columns[0]]
        else:
            averaged_columns[coords] = cleaned_df[columns].mean(axis=1, skipna=True)

    # Create a new DataFrame for the averaged columns
    averaged_sensor_data_df = pd.DataFrame(averaged_columns)

    # Now create a DataFrame from the 'index' and 'time' columns
    initial_cols_df = cleaned_df[['index', 'time']]

    # Concatenate the initial_cols_df with the averaged_sensor_data_df to maintain column order
    final_averaged_df = pd.concat([initial_cols_df, averaged_sensor_data_df], axis=1)

    return final_averaged_df


def process_and_clean_sensor_data(file_path):
    # Load the sensor readings from the CSV file into a DataFrame
    sensor_readings_df = pd.read_csv(file_path, header=0)

    # Explicitly rename the first column to 'index'
    sensor_readings_df.rename(columns={sensor_readings_df.columns[0]: 'index'}, inplace=True)

    # Clean the sensor data
    cleaned_df = clean_sensor_data(sensor_readings_df)

    # Average the sensor data
    averaged_df = average_sensor_data(cleaned_df)

    # Define output file path
    output_csv_path = 'cleaned_averaged_sensor_data.csv'

    # Save the cleaned and averaged data back to a new CSV file
    averaged_df.to_csv(output_csv_path, index=False)
    
    # Return the path to the cleaned and averaged data
    return output_csv_path