#!/usr/bin/python
# Cheng-Tsung Lai
# Email: chengtsung.lai@gmail.com
# 4/30/2018

import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Create an Overlap Histogram for Umbrella Sampling')
parser.add_argument('-b', help='Start Value (file name should be #.out)',
                          required=True, dest='start_no')
parser.add_argument('-e', help='End Value (file name should be #.out)',
                          required=True, dest='end_no')
parser.add_argument('-c', help='Target Column (default 2nd column)',
                          required=False, dest='column_no', default=2)
parser.add_argument('-s', help='Step Size (default 1)',
                          required=False, dest='step_size', default=1)
parser.add_argument('-o', help='Output file (default overlap.out)',
                          required=False, dest='outfile_name', default='overlap.out')

args=parser.parse_args()

grid_size = float(args.step_size) / 10
start=float(args.start_no) - float(args.step_size)*2
end=float(args.end_no) + float(args.step_size)*2 + grid_size
column_no=int(args.column_no)-1

z=0
rawdata=np.zeros((999,999))

for i in np.arange(float(args.start_no),float(args.end_no)+float(args.step_size),float(args.step_size)):
    z+=1
    file_name =  str(i) + '.out'
    print 'parsing', file_name, '...' 
    for line in open(file_name):
        temp=line.split()
        value=float(temp[column_no])
        count=0
        for j in np.arange(start,end,grid_size):
            count+=1
            if(value > (j-grid_size) and value <= (j+grid_size)):
		rawdata[z,count]+=1

f=open(args.outfile_name,'w')
for i in range(1,count+1):
    no=str(start + (i-1)*grid_size) + ' '
    f.write(no)

    for j in range(1,z+1):
        if(j==z):
            string = str(rawdata[j][i]) + "\n"
        else:
            string = str(rawdata[j][i]) + " "
        
        f.write(string)

