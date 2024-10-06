import numpy as np
import h5py
import pandas as pd
from netCDF4 import Dataset
from scipy.ndimage import zoom
import json

try:
    ds = Dataset('MOD11_L2.A2024279.0145.061.2024279034513.NRT (1).hdf')
except OSError:
    print("Unable to open the file with netCDF4")

# Open the HDF file
file_path = 'MOD11_L2.A2024279.0145.061.2024279034513.NRT (1).hdf'
dataset = Dataset(file_path, 'r')

# Extract latitude, longitude, and LST
lat = dataset.variables['Latitude'][:]
lon = dataset.variables['Longitude'][:]
lst = dataset.variables['LST'][:]
coordinates = np.column_stack((lat.flatten(), lon.flatten()))

last_three_values = lst[:, -3:]- 273.15 


# Create coordinate pairs
coordinates = np.column_stack((lat.flatten(), lon.flatten()))


def process_array(arr):
    arr = np.array(arr, dtype=object)
    
    processed_array = []
    
    for sub_arr in arr:
        
        count_dashes = list(sub_arr).count(0)
        if count_dashes == len(sub_arr) or count_dashes == 2:
            continue
        
        elif count_dashes == 1:
            sub_arr_list = list(sub_arr)
            non_dash_elements = [float(x) for x in sub_arr_list if x != 0]
            
            median_val = np.median(non_dash_elements)
            
            sub_arr_list[sub_arr_list.index(0)] = median_val
            
            processed_array.append(sub_arr_list)
        else:
            processed_array.append(sub_arr)
    
    processed_array = np.array(processed_array, dtype=float)
    
    return processed_array

def median_of_all_numbers(arr):
    processed_arr = process_array(arr)
    flattened_arr = processed_arr.flatten()
    return np.median(flattened_arr)

newarray = process_array(last_three_values)

median_val = round(median_of_all_numbers(newarray),2)



# Generar JSON para desplegar en el sitio

datos = {
    "median": median_val
}

json_file_path = 'datos.json'  
with open(json_file_path, 'w') as json_file:
    json.dump(datos, json_file, indent=4)

print(f'Median value saved to {json_file_path}.')