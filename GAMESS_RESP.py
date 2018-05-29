#!/usr/bin/python
#
# Cheng-Tsung Lai
# Email: chengtsung.lai@gmail.com
# 5/29/2018

# The following programs are need for this script
# 1. GAMESS
GAMESS_PATH='/home/ahtsung/Programs/gamess/rungms'
GAMESS_SCR_PATH='/home/ahtsung/scr'
# 2. antechamber and resp from AMBER
# 3. openbabel

# Begin of Script
import os
import numpy as np
import argparse

print "\n"
print "+===========================================================+"
print "|         Generate partical charges with GAMESS/RESP        |"
print "|                       Ver. 1.0.529                        |"
print "|-----------------------------------------------------------|"
print "|                                       By: Cheng-Tsung Lai |"
print "|                          E-mail: chengtsung.lai@gmail.com |"
print "|                                   Last updated: 5/29/2018 |"
print "|===========================================================|"
print "| Note: 1. GAMESS optimization/ESP use HF/6-31G* or         |"
print "|          DFT B3LYP/6-31G* (default)                       |"
print "|       2. RESP uses two steps fitting                      |"
print "|       3. Multiplicity: singlets (1), doublets (2), etc.   |" 
print "|                                                           |"
print "| Use -h to show the help message                           |"
print "| Example: GAMESS_RESP.py -fi pdb -i A.pdb                  |"
print "+===========================================================+"
print "\n"

parser = argparse.ArgumentParser(description='Generate partical charges with GAMESS/RESP')
parser.add_argument('-fi', help='Input file format (pdb or mol2)',
                          required=True, dest='file_type')
parser.add_argument('-i', help='Input file',
                          required=True, dest='file')
parser.add_argument('-nc', help='Net Charge (default: 0)',
                          required=False, dest='charge', default=0)
parser.add_argument('-sp', help='Spin multiplicity (default: 1)',
                          required=False, dest='mult', default=1)
parser.add_argument('-qt', help='QM function: (1)B3LYP/6-31G* or (2)HF/6-31G* (default: 1)',
                          required=False, dest='QM_type', default=1)
parser.add_argument('-np', help='Number of CPU core(s) in GAMESS calculation (default: 1)',
                          required=False, dest='cpu', default=1)

args=parser.parse_args()

file = args.file
charge = args.charge
mult = args.mult
qm_type = args.QM_type
cpu = str(args.cpu)
mol2_file = file.split(".")[0] + '_resp.mol2'

if(args.file_type == 'pdb'):
	command = 'babel -h -i pdb ' + file + ' -o gamin a.inp'
else:
	command = 'babel -h -i ml2 ' + file + ' -o gamin a.inp'

os.system(command)

if(mult == 1):
    scf = 'RHF'
else:
    scf = 'ROHF'

# Create GAMESS optimization input file
outfile=open('b.inp', 'w')

texthead = "! Geometry optimization\n" + \
" $CONTRL  ICHARG=" + str(charge) + ' MULT=' + str(mult) + " RUNTYP=OPTIMIZE\n" + \
"          MAXIT=128 UNITS=ANGS MPLEVL=0 EXETYP=RUN\n" + \
"          SCFTYP=" + scf + "\n" + \
"          COORD=UNIQUE\n"
if(qm_type == 1):
    texthead += \
    "          DFTTYP=B3LYP                                 $END\n"
else:
    texthead += \
    "          DFTTYP=NONE                                  $END\n"
texthead += \
" $SCF     DIRSCF=.T. CONV=1.0E-08 FDIFF=.F.            $END\n" + \
" $SYSTEM  TIMLIM=50000 MWORDS=1024 MEMDDI=0            $END\n" + \
" $BASIS   GBASIS=N31 NGAUSS=6 DIFFSP=.F.\n" + \
"          NDFUNC=1 NPFUNC=0                            $END\n" + \
" $STATPT  NSTEP=20 OPTTOL=1.0E-05 HESS=CALC IHREP=19   $END\n" + \
" $GUESS   GUESS=HUCKEL                                 $END\n" + \
" $DATA\n" + \
"optimization\n" + \
"C1\n"

outfile.write(texthead)

for line in open('a.inp'):
	temp=line.split()
	if(len(temp) == 5):
		outfile.write(line)

outfile.write(" $END\n")
outfile.close()

# Run GAMESS
print '\nStarting optimization using '+ cpu + ' core(s). This step is the most time-consuming step\n'

command = 'rm ' + GAMESS_SCR_PATH + '/b.*'
os.system(command)
command = GAMESS_PATH + ' b 00 ' + cpu + ' > opt.log'
os.system(command)

print "Finished optimization\n";

error_check = 0
for line in open('opt.log'):
	temp = line.split()
	# ddikick.x: Execution terminated due to error(s).
	if(len(temp) >=5 and temp[0] == 'ddikick.x:' and temp[5] == 'error(s).'):
		print 'Running GAMESS faces problem...\n'
		print 'Please check opt.log for details\n'
		error_check +=1

if(error_check == 0):
    os.system("babel -i gamout opt.log -o gamin c.inp")

if(error_check == 0):
# Create GAMESS ESP input file
    outfile=open('d.inp', 'w')

    texthead="! Single point to get ESP\n" + \
    " $CONTRL ICHARG=" + str(charge) + " MULT=" + str(mult) + " RUNTYP=ENERGY MOLPLT=.T.\n" + \
    "         MPLEVL=0 UNITS=ANGS MAXIT=128 EXETYP=RUN\n" + \
    "         SCFTYP=" + scf + "\n" + \
    "         COORD=UNIQUE\n"
    if(qm_type == 1):
        texthead += \
        "          DFTTYP=B3LYP                                 $END\n"
    else:
        texthead += \
        "          DFTTYP=NONE                                  $END\n"
    texthead += \
    " $SCF    DIRSCF=.T. CONV=1.0E-07                       $END\n" + \
    " $SYSTEM TIMLIM=5000 MWORDS=1024 MEMDDI=0              $END\n" + \
    " $BASIS  GBASIS=N31 NGAUSS=6 NDFUNC=1                  $END\n" + \
    " $GUESS  GUESS=HUCKEL                                  $END\n" + \
    " $ELPOT  IEPOT=1 WHERE=PDC OUTPUT=PUNCH                $END\n" + \
    " $PDC    PTSEL=CONNOLLY CONSTR=CHARGE\n" + \
    "         VDWSCL=1.4 VDWINC=0.2 LAYER=4 PTDENS=0.28     $END\n" + \
    " $DATA\n" + \
    "ESP\n" + \
    "C1\n"

    outfile.write(texthead)
    for line in open('c.inp'):
        temp=line.split()
        if(len(temp) ==5):
            outfile.write(line)

    outfile.write(" $END\n")
    outfile.close()

# Run GAMESS
    print "Starting ESP\n";
    command = 'rm ' + GAMESS_SCR_PATH + '/d.*'
    os.system(command)
    command = GAMESS_PATH + ' d 00 ' + cpu + ' > esp.log'
    os.system(command)
    command = 'cp ' + GAMESS_SCR_PATH + '/d.dat esp.dat'
    os.system(command)
    os.system("babel -i gamout esp.log -o ml2 e.mol2")
    print "Finished ESP\n";

    for line in open('opt.log'):
        temp = line.split()
        # ddikick.x: Execution terminated due to error(s).
        if(len(temp) >=5 and temp[0] == 'ddikick.x:' and temp[5] == 'error(s).'):
            print 'Running GAMESS faces problem...\n'
            print 'Please check esp.log for details\n'
            error_check +=1

if(error_check ==0):
# Process GAMESS punch file
    print "Parsing punch file\n"
    outfile=open('esp.in', 'w')

    grid_tag = 0
    coor_tag = 0
    count = 0
    for line in open('esp.dat'):
	temp=line.split()
	if(len(temp)>=1):
	    if(temp[0] == 'NATOMS='):
	        natoms = int(temp[1])
		grid_tag = 0
		coor_tag = 1
		coor_matrix=np.zeros((natoms,3))

	    if(temp[0] == 'BONDATOMS'):
		coor_tag = 0

	    if(len(temp) >= 7 and temp[3] == 'GRID'):
		ngrids = int(temp[-1]) + 1
		grid_tag = 1
		ESP_matrix=np.zeros((ngrids,4))

	    if(grid_tag == 1 and len(temp) == 5):
		ESP_matrix[int(temp[0])] = (float(temp[4]), float(temp[1]), float(temp[2]), float(temp[3]))

	    if(coor_tag == 1 and len(temp) == 4):
		coor_matrix[count] = (float(temp[1]), float(temp[2]), float(temp[3]))
		count +=1

    coor_matrix *= 1.88972666

    outfile.write("%5d%5d%5s\n" % (natoms, ngrids, charge))

    for i in range(0, natoms):
	outfile.write("                %16.7E%16.7E%16.7E\n" % (coor_matrix[i][0], coor_matrix[i][1], coor_matrix[i][2]))
    for i in range(0, ngrids):
	outfile.write("%16.7E%16.7E%16.7E%16.7E\n" % (ESP_matrix[i][0], ESP_matrix[i][1], ESP_matrix[i][2], ESP_matrix[i][3]))

    outfile.close()

# run resp
    command_text="antechamber -s 0 -dr n -fi mol2 -fo ac -i e.mol2 -o f.ac -nc " + str(charge)
    os.system(command_text)
    os.system("respgen -e 2 -i f.ac -o resp1.in -f resp1")
    os.system("respgen -e 2 -i f.ac -o resp2.in -f resp2")
    os.system("resp -O -i resp1.in -o resp1.out -e esp.in -t resp1.qin")
    os.system("resp -O -i resp2.in -o resp2.out -e esp.in -q resp1.qin -t resp2.qin")
    command = "antechamber -s 0 -dr n -fi ac -fo mol2 -i f.ac -o " + mol2_file + " -c rc -cf resp2.qin"
    os.system(command)

    print "Finished RESP\n"

# zip file and delete temperary files
    command = "tar zcvf " + file + "_resp.tar.gz opt.log esp.dat esp.log esp.in " + mol2_file + ' ' + file
    os.system(command)
    os.system("rm opt.log a.inp b.inp c.inp d.inp e.mol2 f.ac resp1.* resp2.* ANTECHAMBER_* ATOMTYPE.INF punch esout esp.in esp.dat esp.log")
