"""
This file currently takes a hardcoded json file and writes it out as a 
CSV file.
"""

import csv
import json
import time

timestamp = time.strftime('%Y_%m_%d')
infile = 'all_advisories_2021-12-05_0928.json'
outfile = 'Cisco_PSIRT_Advisories_' + timestamp + '.csv'


def get_fieldnames(infile):
    with open(infile, 'r') as json_file:
        json_data = json.load(json_file)
        fieldnames = []
        for keys in json_data[0].keys():
            fieldnames.append(keys)
    return fieldnames


def write_json_to_csv(infile, outile):

    with open(infile) as json_file:
        json_data = json.load(json_file)

        with open(outfile, 'w', newline='') as csv_file:
            fieldnames = get_fieldnames(infile)

            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()

            for row in json_data:
                csv_writer.writerow(row)


write_json_to_csv(infile, outfile)
