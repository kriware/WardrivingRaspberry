# Wardriving with Rasbperry
Wardriving Resources for my Youtube Video

Kismet Version: 2016.07.R1-1

Raspbian Buster armhf

## Downloading Raspbian OS
There are hundreds of thousands of tutorials on how to install RaspbianOS, this will not be another one. Google it.

[Raspbian OS Download](https://www.raspberrypi.com/software/operating-systems/)

## Burning Rasbpian OS with dd command

```bash
sudo dd if=2021-10-30-raspios-bullseye-armhf.img of=/dev/sdX bs=4M conv=fsync status=progress
```

## Configuring `/boot` folder to set up wifi and ssh at system startup

The idea is to configure ssh without turning on the raspberry for the first time, so once the OS is burned, insert the SDcard in the computer to edit the files. To do this you only have to create a empty file in the boot folder called ssh.

In the same way with the wifi settings. Edit the `/etc/dhcpd.conf` file with your Wi-Fi credencials.

Reference: [Enable SSH startup](https://pimylifeup.com/raspberry-pi-enable-ssh-boot/)

Reference: [Setup Wifi](https://pimylifeup.com/raspberry-pi-static-ip-address/)

## UDEV Rules
I create a udev rule so that the devices connected via USB always have the same name and they can be referenced in the Kismet configuration files.

Edit `/lib/udev/rules.d/72-static-name.rules` file as follows (note: idProduct and idVendor in your case will be different, look them up using the command lsusb):
```bash
ACTION=="add", SUBSYSTEM=="net", SUBSYSTEMS=="usb", ATTRS{idVendor}=="<your_id>", ATTRS{idProduct}=="<your_id>", NAME="wifi_2ghz"
ACTION=="add", SUBSYSTEM=="net", SUBSYSTEMS=="usb", ATTRS{idVendor}=="<your_id>", ATTRS{idProduct}=="<your_id>", NAME="wifi_5ghz"
```
also GPS usb device:
```bash
ACTION=="add", SUBSYSTEM=="tty", SUBSYSTEMS=="usb", ATTRS{idVendor}=="<your_id>", ATTRS{idProduct}=="<your_id>", MDOE="0666”, SYMLINK+=”gps”
```
[List of wifi card for hacking](https://github.com/v1s1t0r1sh3r3/airgeddon/wiki/Cards%20and%20Chipsets)

To reload udev without reset Rasbperry:
```bash
udevadm control --reload-rules
```

## GPS setup
To setup the GPS device, install the following software:
```bash
sudo apt-get update
sudo apt-get install gpsd gpsd-clients python-gps
sudo apt install gpsd gpsd-tools gpsd-clients
```
The daemon will already be running, to check that the gps is running: 
```bash
cgps -s
```
or:
```bash
gpsmon
```


References: [Setting Up Gpsd On Your RaspberryPi](https://michaelbergeron.com/blog/gpsd-raspberrypi)

## Kismet

Install Kismet with `apt`:
```bash
sudo apt install kismet
```
Edit the file `/etc/kismet/kismet.conf` as following:
```bash
source=wifi_2ghz:channel_hop=true,channels="1,2,3,4,5,6,7,8,9,10,11”
source=wifi_5ghz:channel_hop=true,channels="36,40,44,48,52,56,60,64,100,104,108,112,116, 120, 128, 132, 136, 140, 144, 149”
gps=serial:device=/dev/gps,name=gps_usb
```
The numbers separated by commas are the wifi channels and I am assigning the 2ghz channels to one card and the 5ghz channels to the other.

You can confirm which channels your card supports with the command `iwlist channel`

## Run Kismet and collect data
Run kismet with the configuration file:
```bash
kismet_server -f /etc/kismet/kismet.conf &
```

Maybe I'm forgetting something, I always keep an eye on Twitter @kriwarez for any questions. 
