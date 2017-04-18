#!/usr/bin/env python

# We are in the base of the repo https://github.com/researchapps/funglab
echo $PWD
# /home/vanessa/Documents/Dropbox/Code/researchapps/funglab

# This is the top level data folder for one subject, with scans S1 and S2
# I would recommend on the cluster having a higher level "inputs" or "raw" folder
DATA_FOLDER=/home/vanessa/Documents/Work/pipelines/ryan/sub-01

# This is the output folder we are going to save converted subjects into
OUTPUT_FOLDER=/home/vanessa/Documents/Work/pipelines/bids

# sub-01 should have the general format sub-[uniqueid] where uniqueid can
# be any standard / format you are using for your study.

# First we want to convert from this folder structure to BIDS.
dcm2nii $DATA_FOLDER

ls $DATA_FOLDER

# 20170216_162102FLUMAZENILAUTISM020320s005a1001.nii.gz    # original anatomical
# 20170216_162102s403a000.nii.gz                           # PET
# co20170216_162102FLUMAZENILAUTISM020320s005a1001.nii.gz  # This is reoriented and cropped
# o20170216_162102FLUMAZENILAUTISM020320s005a1001.nii.gz   # This is reoriented
# S1
# S2

python scripts/01.bids_convert.py $DATA_FOLDER $OUTPUT_FOLDER

