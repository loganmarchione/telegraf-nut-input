#!/usr/bin/env python3

import subprocess  # nosec B404
import sys


def get_upsc_data(full_name: str) -> str:
    """
    Get data from upsc command for the specified UPS

    Args:
        full_name (str): UPS name in the format 'ups_name@hostname'

    Returns:
        str: The stdout output from upsc command

    Raises:
        subprocess.CalledProcessError: If upsc command fails
    """
    try:
        # Get the data from upsc
        result = subprocess.run(
            ["/usr/bin/upsc", full_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
            text=True,
            check=True
        )  # nosec B603
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to retrieve data for {full_name}", file=sys.stderr)
        print(e.stderr, file=sys.stderr)
        raise


def format_to_influxdb(upsc_data: str, ups_name: str) -> str:
    """
    Format upsc data into InfluxDB line protocol format

    Args:
        upsc_data (str): Output from upsc command
        ups_name (str): Name of the UPS

    Returns:
        str: Data formatted in InfluxDB line protocol
    """
    # Create an empty list
    data_points = []
    # Different manufacturers use different values (floats vs strings) for specific fields
    # Matches device.serial, ups.serial, ups.vendorid, etc...
    string_keys = {".serial", ".vendorid", ".model"}

    # For each line in the standard output
    for line in upsc_data.splitlines():
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
    return f"ups,ups_name={ups_name} " + ",".join(data_points)


def main() -> int:
    """
    Main function that parses command-line arguments and runs the program

    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    # If an argument isn't supplied, exit
    if len(sys.argv) <= 1:
        print('ERROR: Please include a valid NUT UPS name (example: input.py ups_name@localhost)')
        return 1

    # Set the UPS name from an argument
    full_name = sys.argv[1]
    ups_name = full_name.split('@')[0]

    try:
        # Get data from upsc
        upsc_data = get_upsc_data(full_name)

        # Format the data for InfluxDB
        influxdb_line = format_to_influxdb(upsc_data, ups_name)

        # Output the formatted data
        print(influxdb_line)
        return 0
    except subprocess.CalledProcessError:
        return 1


if __name__ == "__main__":
    sys.exit(main())