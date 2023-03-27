#!/usr/bin/env python3

import subprocess
import sys

final = ""

# If an argument isn't supplied, exit
if len(sys.argv) <= 1:
    print('Please include a valid NUT UPS name\n  Example: input.py ups_name@localhost')
    sys.exit(1)

# Set the UPS name from an argument and host
full_name = sys.argv[1]
ups_name = full_name.split('@')[0]

# Get the data from upsc
data = subprocess.run(["/usr/bin/upsc", full_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

# For each line in the standard output
for line in data.stdout.splitlines():
    # Replace ": " with a ":", then separate based on the colon (example below)
    # battery.type: PbAc
    # ^^key^^       ^^value^^
    line = line.replace(': ', ':')
    key = line.split(':')[0]
    value = line.split(':')[1]

    # Different manufacturers use different values (floats vs strings) for specific fields
    # Matches device.serial, ups.serial, and ups.vendorid
    matches = [".serial", ".vendorid"]

    # First, check for any keys containing strings from above and set those values to strings
    if any(x in key for x in matches):
        value = f'"{value}"'
    else:
        try:
            # If the value is a float, ok
            float(value)
        except ValueError:
            # If the value is not a float (i.e., a string), then wrap it in quotes (this is needed for Influx's line protocol)
            value = f'"{value}"'

    # Create a single data point, then append that data point to the string
    data_point = f"{key}={value},"
    final += data_point

# Format is "measurment tag field(s)", stripping off the final comma
print("ups,"+"ups_name="+ups_name, final.rstrip(','))
