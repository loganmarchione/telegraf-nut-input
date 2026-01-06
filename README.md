# telegraf-nut-input

[![CI](https://github.com/loganmarchione/telegraf-nut-input/actions/workflows/main.yml/badge.svg)](https://github.com/loganmarchione/telegraf-nut-input/actions/workflows/main.yml)

Gets data from [Network UPS Tools (NUT)](https://networkupstools.org/), sends the results to InfluxDB via Telegraf. This is a modified version of [this repo](https://github.com/spidertyler2005/ups-telegraf/tree/patch-1).

## Explanation

  - This is a Python3 script that gets data from NUT, via the `upsc` command, then writes that data to standard output. The output is in InfluxDB's [line protocol](https://docs.influxdata.com/influxdb/v1.8/write_protocols/line_protocol_reference/#) format.
  - This script is meant to run via Telegraf, which then writes the data to InfluxDB (you can later graph this data with Grafana or Chronograf).
  - No user data (UPS names, usernames, passwords, database connections, etc...) is stored in the Python script. Everything is setup in the `telegraf.conf` file.

## Requirements

  - You must already have a working instance of NUT, with Telegraf installed on the same machine.
  - InfluxDB v1
    - You must already have an InfluxDB database and a user that has `WRITE` permissions on that database.
  - InfluxDB v2
    - You must already have an org, bucket, and API token with write access to that bucket.
  - Telegraf needs to be able to reach that InfluxDB instance by hostname or IP address.

### Example usage

Below is an example of manually running the script, and the output it generates.
```
root@nut01:~# python3 input.py apc1@localhost
ups,ups_name=apc1 battery.charge=100,battery.charge.low=10,battery.charge.warning=50,battery.date="2001/09/25",battery.mfr.date="2021/08/14",battery.runtime=4860,battery.runtime.low=120,battery.type="PbAc",battery.voltage=27.3,battery.voltage.nominal=24.0,device.mfr="American Power Conversion",device.model="Back-UPS RS 1500MS2",device.serial="ABCDEFG12345",device.type="ups",driver.name="usbhid-ups",driver.parameter.pollfreq=30,driver.parameter.pollinterval=15,driver.parameter.port="auto",driver.parameter.synchronous="auto",driver.version="2.8.0",driver.version.data="APC HID 0.98",driver.version.internal=0.47,driver.version.usb="libusb-1.0.26 (API: 0x1000109)",input.sensitivity="medium",input.transfer.high=144,input.transfer.low=88,input.voltage=122.0,input.voltage.nominal=120,ups.beeper.status="disabled",ups.delay.shutdown=20,ups.firmware="969.e2 .D",ups.firmware.aux="e2",ups.load=9,ups.mfr="American Power Conversion",ups.mfr.date="2021/08/14",ups.model="Back-UPS RS 1500MS2",ups.productid=0002,ups.realpower.nominal=900,ups.serial="ABCDEFG12345",ups.status="OL",ups.test.result="No test initiated",ups.timer.reboot=0,ups.timer.shutdown=-1,ups.vendorid="051d"
```

Below is an example `telegraf.conf` file to output the data to InfluxDB v1.8 and lower (using username/password) and InfluxDB v2.0 and higher (using API token).
```
###############################################################################
#                            OUTPUT PLUGINS                                   #
###############################################################################

[[outputs.influxdb]]
  urls = ["http://server_name_or_IP:8086"]

  database = "your_database_name_here"

  skip_database_creation = true

  retention_policy = ""

  timeout = "5s"

  username = "username_goes_here"
  password = "password_goes_here"

[[outputs.influxdb_v2]]
  urls = ["http://server_name_or_IP:8086"]

  token = "token_goes_here"

  organization = "org_goes_here"

  bucket = "bucket_goes_here"

  timeout = "5s"

###############################################################################
#                            INPUT PLUGINS                                    #
###############################################################################

 [[inputs.exec]]
   commands = [
     "python3 /custom/scripts/telegraf-nut-input/input.py apc1@localhost"
   ]

   timeout = "5s"

   data_format = "influx"
```

Below is an example of the kinds of data you can graph (this is Grafana).

![Screenshot](https://github.com/loganmarchione/telegraf-nut-input/raw/master/grafana.png)

## Development

```
# virtual environment
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements-dev.txt

# update code

# run checks
make check
```
