# Setting up the Raspberry Pi W as an ethernet gadget

## Headless Raspbian Lite Install
As we will never plug peripherals into the Pi, a headless install of the Raspberry OS will be ideal. To install pretty much follow [this](https://www.tomshardware.com/uk/reviews/raspberry-pi-headless-setup-how-to,6028.html) great guide.

Things to note:
- Choose Raspberry Pi Lite 32 bit, as we don't need the GUI
- Skip `Headless Wi-Fi / Ethernet`, going stright to `Direct USB Connection`
- You may find that the PC recognises the Pi as a COM device, not ethernet device. In this case install and unpack the driver
 [here](https://www.catalog.update.microsoft.com/Search.aspx?q=usb%5Cvid_0525%26pid_a4a2), and update the driver of the COM device to use these. 

