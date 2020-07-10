from bids import BIDSLayout
from bids.tests import get_test_data_path
import os
import json
import logging

path_warning_log = './WARNING.log'
logging.basicConfig(filename=path_warning_log, format='%(levelname)s:%(message)s', level=logging.DEBUG)

data_path = './'

# Initialize the layout
layout = BIDSLayout(data_path)

Contrast = 'T1w'
query = layout.get(suffix=Contrast,extension='nii.gz')

path_specs = './code/specs.json'

with open(path_specs) as json_file:
    data = json.load(json_file)

#Loop across the contrast images to check parameters
for item in query:
    if 'Manufacturer' in item.get_metadata():
        Manufacturer=item.get_metadata()['Manufacturer']
        if Manufacturer in data.keys():
            ManufacturersModelName = item.get_metadata()['ManufacturersModelName']
            if ManufacturersModelName in data[Manufacturer].keys():
                if 'SoftwareVersions' in item.get_metadata():
                    SoftwareVersions=item.get_metadata()['SoftwareVersions']
                RepetitionTime=item.get_metadata()['RepetitionTime']
                if Manufacturer != 'GE':
                    if data[Manufacturer][ManufacturersModelName][str(Contrast)]["RepetitionTime"] != RepetitionTime:
                        logging.warning(' Incorrect RepetitionTime: ' + item.filename + '; TR=' + str(RepetitionTime) + ' instead of ' + str(data[Manufacturer][ManufacturersModelName][str(Contrast)]["RepetitionTime"]))
                EchoTime=item.get_metadata()['EchoTime']
                if Manufacturer != 'GE':
                    if data[Manufacturer][ManufacturersModelName][str(Contrast)]["EchoTime"] != EchoTime:
                        logging.warning(' Incorrect EchoTime: ' + item.filename + '; TE=' + str(EchoTime) + ' instead of ' + str(data[Manufacturer][ManufacturersModelName][str(Contrast)]["EchoTime"]))
                FlipAngle=item.get_metadata()['FlipAngle']
                if data[Manufacturer][ManufacturersModelName][str(Contrast)]["FlipAngle"] != FlipAngle:
                    logging.warning(' Incorrect FlipAngle: ' + item.filename + '; FA=' + str(FlipAngle) + ' instead of ' + str(data[Manufacturer][ManufacturersModelName][str(Contrast)]["FlipAngle"]))
            else:
                logging.warning('Missing: '+ ManufacturersModelName)
    else:
       logging.warning('Missing Manufacturer in json sidecar')

#Print WARNING log
if path_warning_log :
    file = open(path_warning_log, 'r')
    lines = file.read().splitlines()
    file.close()
    for line in lines:
        print(line)
        
