#!/usr/bin/env python

import os
import re
import sys
import nibabel
import pandas
import json

from glob import glob

# These arguments come from the command line. You should first
# run this interactively (eg with ipython in a terminal) and 
# type/copy paste the commands one at a time.
# /home/vanessa/Documents/Work/pipelines/ryan/sub-01
data_folder = sys.argv[1]
output_folder = sys.argv[2]

# Here we are making sure that output folders and data folders exist
# and making them if necessary
if not os.path.exists(output_folder):
    os.mkdir(output_folder)
    print("Creating output folder %s" %(output_folder))

if not os.path.exists(data_folder):
    print("Cannot find %s. Check path and try again" %(data_folder))

# This is the subject id, and we are extracting from the folder name
sub_id = os.path.basename(data_folder) # You can also extract this from the data


# Here we are preparing output BIDS folders
bids_folder = "%s/%s" %(output_folder,sub_id)
if not os.path.exists(bids_folder):
    print("Making bids output folder %s" %(bids_folder))
    os.mkdir(bids_folder)

for folder in ['anat','pet']:
    modality_folder = "%s/%s" %(bids_folder,folder)
    if not os.path.exists(modality_folder):
        os.mkdir(modality_folder)


# S1 has the anatomicals
anat_files = glob('%s/S1/*.nii.gz' %data_folder)

# S2 has the pet
pet_file = glob('%s/S2/*.nii.gz' %data_folder)[0]


# Let's use this anatomical
anat_file = [x for x in anat_files if re.search('^co',os.path.basename(x))][0]
anat_bids = "%s/anat/%s_T1w.nii.gz" %(bids_folder,sub_id)
os.rename(anat_file,anat_bids)

# And rename the pet
pet_bids = "%s/pet/%s_pet.nii.gz" %(bids_folder,sub_id)
os.rename(pet_file,pet_bids)

# RYAN: here is where you start!
# Now we want to generate a json data structure for each of these files to be finished.
# Step 1: Download this example pet data in BIDS Format: https://drive.google.com/file/d/0B2JWN60ZLkgkOHdxRk5BUUlQelE/view?usp=sharing
# Step 2: Look at the json file in /pet_phno/sub-000005/pet/. This is the file that you will want to create for your pet data,
# and the equivalent for the T1 (see in the anat folder). 
# Step 3: Read in your nifti output files generated above as follows:

anat = nibabel.load(anat_bids)
pet = nibabel.load(pet_bids)

# Take a look at pet.header.keys() that can be accessed in the header, and read about
# nibabel here: http://nipy.org/nibabel/
# Your goal is to generate that json file, name equivalently as the example, and save
# each one to the anat / pet folder respectively. Use the write_json function below 
# to save your dictionary. So for example, you could do:

anat_dict = dict()
anat_dict["Info"] = dict()
anat_dict["Info"]["BodyPart"] = "brain"

# FILL IN THE REST HERE

# Save, each of anat and pet


# Final Step
# Generation of BIDS information

bids_description = { "BIDSVersion": "1.1.0-pet",
                     "Name": "FLUMAZENILAUTISM" }
bids_description_file = "%s/dataset_description.json" %bids_folder

# Here is a function to write a json file
def write_json(json_obj,filename,mode="w",print_pretty=True):
    '''write_json will (optionally,pretty print) a json object to file
    :param json_obj: the dict to print to json
    :param filename: the output file to write to
    :param pretty_print: if True, will use nicer formatting   
    '''
    with open(filename,mode) as filey:
        if print_pretty == True:
            filey.writelines(json.dumps(json_obj, indent=4, separators=(',', ': ')))
        else:
            filey.writelines(json.dumps(json_obj))
    return filename


# Write the file
write_json(bids_description,bids_description_file)

# Write participants file
participants_file = "%s/participants.tsv" %(bids_folder)
if os.path.exists(participants_file):
    participants = pandas.read_csv(participants_file,index=True,sep="\t")
else:
    participants = pandas.DataFrame(columns=["participant_id","species","strain","population",
                                             "bodyWeight","bodyWeightUnits","age","ageUnits","gender"])

participants.loc[sub_id,"participant_id"] = sub_id
participants.to_csv(participants_file,sep="\t")

