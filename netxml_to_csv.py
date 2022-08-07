#!/usr/bin/env python3

# Author: Cristian Cantos

import sys
import argparse
import xml.etree.ElementTree as ET


def parse_arguments():
    try:
        parser = argparse.ArgumentParser(description="Converts a Kismet results file from XML to CSV format")
        requiredNamed = parser.add_argument_group('required named arguments')
        requiredNamed.add_argument('-i', '--input', help="Input XML file", required=True)
        requiredNamed.add_argument('-o', '--output', help="Output CSV file", required=True)
        args, unknown = parser.parse_known_args()
        return args
    except ValueError:
        parser.print_help()
        sys.exit(1)

def main():
    args = parse_arguments()
    inputFile = args.input
    outputFile = args.output
    with open(outputFile, 'w', encoding='utf-8') as csv:
        csv.write("SSID,Mac,Encryption,Latitude,Longitude")
        try:
            tree = ET.parse(inputFile)
            root = tree.getroot()
            for child in root:
                if child.tag == "wireless-network":
                    essid = ""
                    mac_address = ""
                    encryption = []
                    Latitude = ""
                    Longtitude = ""
                    for wireless_network in child:
                        # Each encryption essid
                        if wireless_network.tag == "SSID":
                            for ssid in wireless_network:
                                if ssid.tag == "encryption":
                                    encryption.append(str(ssid.text))
                                elif ssid.tag == "essid":
                                    essid = str(ssid.text)

                        if wireless_network.tag == "BSSID":
                            mac_address = str(wireless_network.text)

                        if wireless_network.tag == "gps-info":
                            for gps in wireless_network:
                                if gps.tag == "avg-lat":
                                    Latitude = str(gps.text)
                                if gps.tag == "avg-lon":
                                    Longtitude = str(gps.text)

                        encryption.sort()

                    if encryption:
                        essid = essid.replace(',', '.')
                        if essid != "":
                                csv.write("\n" + essid + "," + mac_address + "," + ' '.join(encryption) + "," + Latitude + "," + Longtitude)
                        else:
                                csv.write("\nhidden," + mac_address + "," + ' '.join(encryption) + "," + Latitude + "," + Longtitude)

        except ET.ParseError:
            sys.exit(1)


if __name__ == '__main__':
    main()
