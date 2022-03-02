# Open Hardware Monitor Display

The aim of this project was to use the 16x16 matrix to show CPU & GPU load % and temperature readouts from the connected PC. Using [Open Hardware Monitor](https://openhardwaremonitor.org/), we can easily get this data by querying the server that can be exposed.

The [config file](../config/config.json) contains the routes to each node in the returned data, the IP:port address of the PC to query and a "min temp" value, that tells the display when to show the readouts.

## Configuration

### Open Hardware Monitor

To provide a seamless integration, it is advised to once installed, set the following Options on:
- Start Minimized
- Minimize To Tray
- Minimize On Close
- Run On Windows Startup
- **Remote Web Server** (the only required part)
  - **Run**

You must ensure 8085 is open on your firewall to accept connections.

Also, ensuring the PC to measure has a static IP will mean the integration won't suddenly break!

### config.json

For the application to find the correct values, we need to set the ordered list of nodes to traverse. This can be found by looking at the Open HW Monitor output (or manually going to <ip>:8085/data.json). They usually start:
- Sensor
- PC Name
- Component (GCP/CPU name)
- Temperature/Load
- The specific metric - you can choose whichever you want to show

Set the `addr` to the ip of the PC and the port (default 8085).

Min Temp can be as low or high as you want. Whenever the CPU or GPU reaches or exceeds the minimum temperature set, the display will show this. 

