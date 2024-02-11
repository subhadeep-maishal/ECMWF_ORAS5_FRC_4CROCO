import os
import xarray as xr

# Befor download data using ECMWF_OCEAN5_request.py
# extract file 
# tar-xvzf multi_lev_final.tar.gz 
# tar -xvzf single_lev_final.tar.gz

#Further Information:  http://www.croco-ocean.org

# developed by Subhadeep Maishal
# Indian Institute of Technology, Kharagpur
# subhadeepmaishal@kgpian.iitkgp.ac.in

# Set start and end dates (user need to modify)
YEAR_START = 2022
MONTH_START = 1

YEAR_END = 2022
MONTH_END = 12

# Set input and output directories (user need to modify)
INPUT_DIR = "/scratch/20cl91p02/CROCO_TOOL_FIX/ORAS5_monthly_Oforc_ECMWF_OCEAN5"
OUTPUT_DIR = "output_files"

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# List of variable names
variable_names = ["sossheig", "vomecrtn", "vosaline", "votemper", "vozocrte"]

# Loop through each month in the specified range
for year in range(YEAR_START, YEAR_END + 1):
    for month in range(MONTH_START, MONTH_END + 1):
        current_month = f"{year}{month:02d}"

        # Create an empty dataset
        ds_concatenated = None

        # Loop through each variable
        for var in variable_names:
            # Debug information
            print(f"Looking for files matching pattern: {var}_control_monthly_highres_*_{current_month}_OPER_v0.1.nc")

            # Find files for the current variable and month
            current_files = [f for f in os.listdir(INPUT_DIR) if f.startswith(f"{var}_control_monthly_highres") and current_month in f]

            # Add files to the dataset
            if current_files:
                print(f"Found files: {current_files}")
                ds_current = xr.open_mfdataset([os.path.join(INPUT_DIR, file) for file in current_files])
                if ds_concatenated is None:
                    ds_concatenated = ds_current
                else:
                    ds_concatenated = xr.concat([ds_concatenated, ds_current], dim="time_counter")
            else:
                print(f"No files found for {var} and month {current_month}")
                # If any variable is missing, exit the loop for the current month
                break

        # Check if all variables are present for the current month
        if ds_concatenated is not None:
            # Save concatenated dataset to a new NetCDF file
            output_file = os.path.join(OUTPUT_DIR, f"ECMWF_ORAS5_{current_month}.nc")
            ds_concatenated.to_netcdf(output_file)

            # Rename variables in the final output file
            ds_renamed = ds_concatenated.rename_vars({'sossheig': 'zos', 'votemper': 'thetao', 'vomecrtn': 'uo', 'vozocrte': 'vo', 'vosaline': 'so'})
            ds_renamed.to_netcdf(output_file)

            print(f"Concatenation completed successfully. Output file: {output_file}")
        else:
            print("Not all variables found in each file. Skipping concatenation.")

        # Print a separator for better readability
        print("------------------------------------------")

