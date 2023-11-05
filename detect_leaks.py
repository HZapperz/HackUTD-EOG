import pandas as pd
import numpy as np

sensor_coords = {
    '40.595561_-105.14055': (40.595561, -105.14055),
    '40.596108_-105.140583': (40.596108, -105.140583),
    '40.595556_-105.140069': (40.595556, -105.140069),
    '40.596114_-105.140075': (40.596114, -105.140075),
    '40.595561_-105.14055': (40.595561, -105.14055),
    '40.595658_-105.139869': (40.595658, -105.139869),
    '40.595725_-105.140008': (40.595725, -105.140008),
    '40.595881_-105.139686': (40.595881, -105.139686),
    '40.595947_-105.139833': (40.595947, -105.139833),
    '40.595542_-105.139211': (40.595542, -105.139211),
    '40.595547_-105.139714': (40.595547, -105.139714),
    '40.596089_-105.139144': (40.596089, -105.139144),
    '40.596097_-105.139678': (40.596097, -105.139678)
}

site_coords = {
    "5S": (40.595928, -105.139408),
    "5W": (40.595665, -105.139416),
    "4T": (40.595800, -105.139869),
    "4W": (40.595938, -105.140323),
    "4S": (40.595639, -105.140304)
}

def triangulate_methane_leak(leak_readings):
    # Ensure we have leak readings and at least one sensor has detected a leak
    if leak_readings and any(reading > 1345 for reading in leak_readings.values()):
        # Sort the sensors based on their readings, highest first
        sorted_sensors = sorted(leak_readings.items(), key=lambda item: item[1], reverse=True)
        # Take the top three readings, or fewer if fewer than three sensors detected a leak
        top_sensors = sorted_sensors[:3]

        lat_sum = 0.0
        lon_sum = 0.0
        valid_sensors = 0  # Counter for valid sensors
        for sensor_id, _ in top_sensors:
            # Strip any leading/trailing whitespace from sensor_id
            sensor_id = sensor_id.strip()
            if sensor_id in sensor_coords:
                lat, lon = sensor_coords[sensor_id]
                lat_sum += lat
                lon_sum += lon
                valid_sensors += 1
            else:
                print(f"Warning: Sensor ID {sensor_id} not found in sensor_coords dictionary")

        if valid_sensors == 0:
            return 'None'

        # Calculate the centroid of the triangle formed by the top three sensors
        centroid_lat = lat_sum / valid_sensors
        centroid_lon = lon_sum / valid_sensors

        # Find the closest site to the centroid
        closest_site = min(site_coords, key=lambda site: (site_coords[site][0] - centroid_lat)**2 + (site_coords[site][1] - centroid_lon)**2)
        # Return only the first part of the location identifier (e.g., "5S" or "5W")
        return closest_site.split(' ')[0]
    else:
        return 'None'



def detect_methane_leaks(sensor_reading):
    return sensor_reading > 1345

def get_location(sensor_readings):
    # Extract the sensor readings, ignoring the first two columns (index and timing)
    readings = {sensor: reading for sensor, reading in sensor_readings.items() if sensor not in ['index', 'time']}

    # Perform triangulation to get the leak location
    location_code = triangulate_methane_leak(readings)
    return location_code if location_code != 'None' else ''

def process_sensor_readings(sensor_data_filepath, output_file_path, team_name):
    # Load the sensor data from the CSV file
    sensor_data = pd.read_csv(sensor_data_filepath)

    with open(f"{team_name}_leaks.txt", 'w') as output_file:
        output_file.write("time, location\n")
        for index, row in sensor_data.iterrows():
            time = row['time']
            # Pass a dictionary excluding 'index' and 'time' columns
            sensor_readings = {k: v for k, v in row.items() if k not in ['index', 'time']}
            # Check if any sensor reading is above the threshold for a leak
            if any(value > 1345 for value in sensor_readings.values()):  # Changed line
                location_str = get_location(sensor_readings)
                # Write the time and location(s) to the file
                output_file.write(f"{time}, {location_str}\n")


def process_and_detect_leaks(sensor_data_filepath, team_name):
    # Load the sensor data from the CSV file
    sensor_data = pd.read_csv(sensor_data_filepath)

    # Ensure your team name doesn't contain spaces or special characters
    team_name_clean = ''.join(e for e in team_name if e.isalnum())

    # Define output file path
    output_file_path = f"{team_name_clean}_leaks.txt"

    with open(output_file_path, 'w') as output_file:
        output_file.write("time, location\n")
        for index, row in sensor_data.iterrows():
            time = row['time']
            # Pass a dictionary excluding 'index' and 'time' columns
            sensor_readings = {k: v for k, v in row.items() if k not in ['index', 'time']}
            # Check if any sensor reading is above the threshold for a leak
            if any(value > 1345 for value in sensor_readings.values()):
                location_str = get_location(sensor_readings)
                # Write the time and location(s) to the file
                output_file.write(f"{time}, {location_str}\n")

    # Return the path to the leaks file
    return output_file_path