# telegraf-nut-input

[![CI](https://github.com/loganmarchione/telegraf-nut-input/actions/workflows/main.yml/badge.svg)](https://github.com/loganmarchione/telegraf-nut-input/actions/workflows/main.yml)

Gets data from [Network UPS Tools (NUT)](https://networkupstools.org/), sends the results to InfluxDB via Telegraf. This is a modified version of [this repo](https://github.com/spidertyler2005/ups-telegraf/tree/patch-1).

## Explanation

  - This is a Python3 script that gets data from NUT, via the `upsc` command, then writes that data to standard output. The output is in InfluxDB's [line protocol](https://docs.influxdata.com/influxdb/v1.8/write_protocols/line_protocol_reference/#) format.
  - This script is meant to run via Telegraf, which then writes the data to InfluxDB (you can later graph this data with Grafana or Chronograf).
  - No user data (UPS names, usernames, passwords, database connections, etc...) is stored in the Python script. Everything is setup in the `telegraf.conf` file.

## Requirements

  - You must already have a working instance of NUT, with Telegraf installed on the same machine.
  - You must already have an InfluxDB database created, along with a user that has `WRITE` and `READ` permissions on that database.
  - Telegraf needs to be able to reach that InfluxDB instance by hostname or IP address.

### Example usage

Below is an example of manually running the script, and the output it generates.
```
root@test04:~# python3 input.py cyberpower1@localhost
ups,ups_name=cyberpower1 battery.charge=100,battery.charge.low=10,battery.charge.warning=20,battery.mfr.date="CPS",battery.runtime=7140,battery.runtime.low=300,battery.type="PbAcid",battery.voltage=24.0,battery.voltage.nominal=24,device.mfr="CPS",device.model="CP1500PFCLCD",device.serial=000000000000,device.type="ups",driver.name="usbhid-ups",driver.parameter.pollfreq=30,driver.parameter.pollinterval=15,driver.parameter.port="auto",driver.parameter.synchronous="no",driver.version="2.7.4",driver.version.data="CyberPower HID 0.4",driver.version.internal=0.41,input.transfer.high=139,input.transfer.low=88,input.voltage=120.0,input.voltage.nominal=120,output.voltage=136.0,ups.beeper.status="disabled",ups.delay.shutdown=20,ups.delay.start=30,ups.load=5,ups.mfr="CPS",ups.model="CP1500PFCLCD",ups.productid=0501,ups.realpower.nominal=900,ups.serial=000000000000,ups.status="OL",ups.test.result="No test initiated",ups.timer.shutdown=-60,ups.timer.start=-60,ups.vendorid=0764
```

Below is an example `telegraf.conf` file to output the data to InfluxDB.
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

###############################################################################
#                            INPUT PLUGINS                                    #
###############################################################################

 [[inputs.exec]]
   commands = [
     "python3 /custom/scripts/telegraf-nut-input/input.py cyberpower1@localhost"
   ]

   timeout = "5s"

   data_format = "influx"
```

Below is an example of the kinds of data you can graph (this is Grafana).
![Screenshot](https://github.com/loganmarchione/telegraf-nut-input/raw/master/grafana.png)

## TODO
- [ ] Find a more elegant way to transform raw `upsc` output into key/value pairs
- [ ] Make a list of specific values to look for (I'm currently sending every value from `upsc` to Telegraf)
- [ ] Keep watching [this issue](https://github.com/influxdata/telegraf/issues/6316), which would be a more ideal way to get data from NUT
- [x] Add linting with Travis CI
- [x] Make the Python script fail if there isn't an argument
