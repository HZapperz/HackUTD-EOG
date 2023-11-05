import streamlit as st
from clean_sensor import clean_sensor_data, average_sensor_data
from detect_leaks import process_and_detect_leaks
import pandas as pd

# Set page config to add a title and potentially a favicon
st.set_page_config(page_title="Methane Leak Analysis - KTP", page_icon=None)

# Add a title at the top of the app
st.title("Methane Leak Analysis - KTP")

# Your Streamlit code to upload the file
uploaded_file = st.file_uploader("Choose a CSV file", type='csv')
if uploaded_file is not None:
    # Read the file into a dataframe
    df = pd.read_csv(uploaded_file)
    
    # Process the dataframe with your cleaning scripts
    cleaned_df = clean_sensor_data(df)
    averaged_df = average_sensor_data(cleaned_df)
    
    # Save the processed data to a new CSV file
    processed_data_filepath = 'processed_sensor_data.csv'
    averaged_df.to_csv(processed_data_filepath, index=False)

    # Call your leak detection function
    team_name = "Methane Leak Analysis - KTP"
    output_file_path = process_and_detect_leaks(processed_data_filepath, team_name)
    
    # Display the results and allow the user to download the output file
    try:
        with open(output_file_path, "r") as file:
            leak_detections = file.read()
            
            # Display the contents of the output file in a text area
            st.text_area("Leak Detection Results", leak_detections, height=300)
            
            # Create a download link for the output file
            st.download_button(
                label="Download Leak Detection Results",
                data=file,
                file_name="leak_detection_results.txt",
                mime="text/plain"
            )
    except Exception as e:
        st.error(f"An error occurred when reading the output file: {e}")

# Below are some additional UI enhancement suggestions:

# Add a sidebar for optional app controls or to display team info
st.sidebar.info("This app is developed by the KTP team specializing in Methane Leak Analysis.")

# Use columns to layout elements in a more visually appealing manner
col1, col2 = st.columns(2)
with col1:
    st.header("Instructions")
    st.markdown("""
        - Upload the CSV file using the provided button.
        - Review the detected leaks in the text area.
        - Download the results using the 'Download' button.
    """)

with col2:
    st.header("About the Analysis")
    st.markdown("""
        - Our algorithms clean and process sensor data according to specifications from [RAM's methane sensor](https://ram-e-shop.com/product/kit-mq4/).
        - Our models detect methane leaks with precision.
        - The output file includes time and location.
    """)
