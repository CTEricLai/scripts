#!/usr/bin/python
#
# Cheng-Tsung Lai
# Email: chengtsung.lai@gmail.com
# 5/23/2018

# The following programs are need for this script
# 1. parmed, tleap from AMBER


# Begin of Script
import os
import numpy as np
import argparse

print "\n"
print "+===========================================================+"
print "|         Generate .lib and .frcmod from mol2 file          |"
print "|-----------------------------------------------------------|"
print "|                                       By: Cheng-Tsung Lai |"
print "|                          E-mail: chengtsung.lai@gmail.com |"
print "|                                   Last updated: 5/23/2018 |"
print "|===========================================================|"
print "| Note: 1. Based on general AMBER force field (GAFF)        |"
print "|       2. Mol2 file must already had partial charges       |"
print "|                                                           |"
print "| Use -h to show the help message                           |"
print "| Example: LIB_FRCMOD.py -i ben.mol2 -n BEN                 |"
print "+===========================================================+"
print "\n"

parser = argparse.ArgumentParser(description='Generate .lib and .frcmod from mol2 file')
parser.add_argument('-i', help='Input file (must be mol2)',
                          required=True, dest='file')
parser.add_argument('-n', help='Ligand name in mol2 file',
                          required=True, dest='lig_name')
parser.add_argument('-g', help='GAFF 1 or 2 (default: 1)', 
                          required=False, dest='gaff_type', default=1)

args=parser.parse_args()

file = args.file
lig_name = args.lig_name
gaff_type = str(args.gaff_type)

# Create .frcmod file
frcmod_file = file.split(".")[0] + '.frcmod'
lib_file = file.split(".")[0] + '.lib'

command = 'parmchk2 -i ' + file + ' -o ' + frcmod_file + ' -f mol2 -a Y -s ' + gaff_type
os.system(command)
print 'Finish generating frcmod file: ' + frcmod_file + '\n'

# Create .lib file
# tleap input file
outfile=open('temp.in', 'w')

texthead = lig_name + '=loadmol2 ' + file + '\n' + \
'saveoff ' + lig_name + ' ' + lib_file + '\n' + \
'quit\n'

outfile.write(texthead)
outfile.close()

command = 'rm ' + lib_file
os.system(command)
os.system("tleap -f temp.in")
os.system("rm temp.in ANTECHAMBER.FRCMOD")
print 'Finish generating lib file: ' + lib_file + '\n'

