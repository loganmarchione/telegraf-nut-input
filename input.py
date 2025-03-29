#!/usr/bin/env python3

import subprocess  # nosec B404
import sys

# If an argument isn't supplied, exit
if len(sys.argv) <= 1:
    print('ERROR: Please include a valid NUT UPS name (example: input.py ups_name@localhost)')
    sys.exit(1)

# Set the UPS name from an argument
full_name = sys.argv[1]
ups_name = full_name.split('@')[0]

try:
    # Get the data from upsc
    data = subprocess.run(["/usr/bin/upsc", full_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, text=True, check=True)  # nosec B603
except subprocess.CalledProcessError as e:
    print(f"ERROR: Failed to retrieve data for {full_name}", file=sys.stderr)
    print(e.stderr, file=sys.stderr)
    sys.exit(1)

# Create an empty list
data_points = []
# Different manufacturers use different values (floats vs strings) for specific fields
# Matches device.serial, ups.serial, ups.vendorid, etc...
string_keys = {".serial", ".vendorid", ".model"}

# For each line in the standard output
for line in data.stdout.splitlines():
    # Skip malformed lines
    if ": " not in line:
        continue

    # We have this example
    # battery.type: PbAc
    # Split based on the colon
    key, value = line.split(":", 1)
    # Remove leading/trailing whitespace from the value
    value = value.strip()

    # Ensure correct formatting for InfluxDB line protocol
    if any(key.endswith(s) for s in string_keys):
        # Wrap specific values in quotes
        value = f'"{value}"'
    else:
         # If it's a float, leave it be
        try:
            float(value)
        # If the value is not a float (i.e., a string), then wrap it in quotes
        except ValueError:
            value = f'"{value}"'

    data_points.append(f"{key}={value}")

# Construct final output
print(f"ups,ups_name={ups_name} " + ",".join(data_points))
