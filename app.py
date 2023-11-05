import streamlit as st
from clean_sensor import clean_sensor_data, average_sensor_data
from detect_leaks import process_and_detect_leaks
import pandas as pd

# Your Streamlit code to upload the file
uploaded_file = st.file_uploader("Choose a CSV file", type='csv')
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    # To convert to a dataframe (assuming that the uploaded file is a csv)
    df = pd.read_csv(uploaded_file)
    
    # Process the dataframe as per your cleaning script
    cleaned_df = clean_sensor_data(df)
    averaged_df = average_sensor_data(cleaned_df)
    
    # Save the processed data to a new CSV file
    processed_data_filepath = 'processed_sensor_data.csv'
    averaged_df.to_csv(processed_data_filepath, index=False)

    # Now, you can call your `process_and_detect_leaks` function
    team_name = "Methane Leak Analysis - KTP"

    output_file_path = process_and_detect_leaks(processed_data_filepath, team_name)
    
    # Read the output file and display its contents
    try:
        with open(output_file_path, "r") as file:
            leak_detections = file.read()
            st.text_area("Leak Detection Results", leak_detections, height=300)
    except Exception as e:
        st.error(f"An error occurred when reading the output file: {e}")
