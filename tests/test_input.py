#!/usr/bin/env python3

import importlib.util

import pytest

# Import the input.py module directly
script_path = "./input.py"
spec = importlib.util.spec_from_file_location("input_module", script_path)
input_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(input_module)

# Sample mock UPS output
# "Init SSL without certificate database" is actually part of the output
MOCK_UPSC_OUTPUT = """Init SSL without certificate database
battery.charge: 100
battery.charge.low: 10
battery.charge.warning: 50
battery.date: 2001/09/25
battery.mfr.date: 2021/08/14
battery.runtime: 4860
battery.runtime.low: 120
battery.type: PbAc
battery.voltage: 27.3
battery.voltage.nominal: 24.0
device.mfr: American Power Conversion
device.model: Back-UPS RS 1500MS2
device.serial: ABCDEFG12345
device.type: ups
driver.name: usbhid-ups
driver.parameter.pollfreq: 30
driver.parameter.pollinterval: 15
driver.parameter.port: auto
driver.parameter.synchronous: auto
driver.version: 2.8.0
driver.version.data: APC HID 0.98
driver.version.internal: 0.47
driver.version.usb: libusb-1.0.26 (API: 0x1000109)
input.sensitivity: medium
input.transfer.high: 144
input.transfer.low: 88
input.voltage: 122.0
input.voltage.nominal: 120
ups.beeper.status: disabled
ups.delay.shutdown: 20
ups.firmware: 969.e2 .D
ups.firmware.aux: e2     
ups.load: 9
ups.mfr: American Power Conversion
ups.mfr.date: 2021/08/14
ups.model: Back-UPS RS 1500MS2
ups.productid: 0002
ups.realpower.nominal: 900
ups.serial: ABCDEFG12345
ups.status: OL
ups.test.result: No test initiated
ups.timer.reboot: 0
ups.timer.shutdown: -1
ups.vendorid: 051d
"""

EXPECTED_OUTPUT = 'ups,ups_name=apc1 battery.charge=100,battery.charge.low=10,battery.charge.warning=50,battery.date="2001/09/25",battery.mfr.date="2021/08/14",battery.runtime=4860,battery.runtime.low=120,battery.type="PbAc",battery.voltage=27.3,battery.voltage.nominal=24.0,device.mfr="American Power Conversion",device.model="Back-UPS RS 1500MS2",device.serial="ABCDEFG12345",device.type="ups",driver.name="usbhid-ups",driver.parameter.pollfreq=30,driver.parameter.pollinterval=15,driver.parameter.port="auto",driver.parameter.synchronous="auto",driver.version="2.8.0",driver.version.data="APC HID 0.98",driver.version.internal=0.47,driver.version.usb="libusb-1.0.26 (API: 0x1000109)",input.sensitivity="medium",input.transfer.high=144,input.transfer.low=88,input.voltage=122.0,input.voltage.nominal=120,ups.beeper.status="disabled",ups.delay.shutdown=20,ups.firmware="969.e2 .D",ups.firmware.aux="e2",ups.load=9,ups.mfr="American Power Conversion",ups.mfr.date="2021/08/14",ups.model="Back-UPS RS 1500MS2",ups.productid=0002,ups.realpower.nominal=900,ups.serial="ABCDEFG12345",ups.status="OL",ups.test.result="No test initiated",ups.timer.reboot=0,ups.timer.shutdown=-1,ups.vendorid="051d"'


def test_format_to_influxdb():
    """Test the format_to_influxdb function with mock data."""
    # Call the function with the mock data
    result = input_module.format_to_influxdb(MOCK_UPSC_OUTPUT, "apc1")

    # Print both result and expected output to help debug
    print("\nActual output:\n", result)
    print("\nExpected output:\n", EXPECTED_OUTPUT)

    # Verify the function returns the expected output
    assert result == EXPECTED_OUTPUT

# other tests to add later
    # get_upsc_data function
    # main function with no args
    # main function

if __name__ == "__main__":
    pytest.main(["-v", __file__])
