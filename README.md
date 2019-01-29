# ThingSet Dashboard
A web app to plot measurement data using influxdb, dash and plotly. This app listens to a serial port, stores incoming measurement data in a local influxdb and displays the data on http://localhost:8050.

## Send raw data from file to pseudo serial
For testing purposes: If measurement data only are available in a text file, open up two interconnected pseudo terminals
```
socat -d -d pty,raw,echo=0 pty,raw,echo=0
```
Send data to first pseudo terminal with
```
python emuserial <port>
```