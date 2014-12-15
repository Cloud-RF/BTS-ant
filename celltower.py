#!/usr/bin/python

# Copyright (c) 2014 Alex Farrant
# Distributed under the GNU GPL v2. 

# Create radiation patterns for multi panel cell towers 
# Requires a single .ant horizontal pattern with 360 rows referenced to 0dB Peak power
import sys

azimuthA=0
azimuthB=120
azimuthC=240
fileout="celltower.ant"

data = []
pattern = []
pattern1 = []
pattern2 = []
pattern3 = []
celltower = []

# Rotation
def rot(l, y=1):
   if len(l) == 0:
      return l
   y = -y % len(l)     # flip rotation direction
   return l[y:] + l[:y]
   
# read in .ant file
with open(sys.argv[1]) as f:
    data = f.readlines()
f.close()

# Crop first 360 degs containing horizontal pattern
for i in range(0,360):
	pattern.append(data[i].replace("\n", "").replace("\t", "").replace(" ", ""))

# Rotate patterns to make our lists
pattern1=rot(pattern,azimuthA)
pattern2=rot(pattern,azimuthB)
pattern3=rot(pattern,azimuthC)

for i in range(0,360):
	# Pick best value to be appended to celltower[]
	
	if float(pattern1[i]) > float(pattern2[i]):
		winner=float(pattern1[i])
		
	if float(pattern2[i]) > float(pattern1[i]):
		winner=float(pattern2[i])
		
	if float(pattern3[i]) > float(winner):
		winner=float(pattern3[i])
	print "%d: %s (%s, %s, %s)" % (i,winner,pattern1[i],pattern2[i],pattern3[i])
	celltower.append(winner) # The winner takes it all...

# Output horizontal pattern
file=open(fileout,'w')	
for row in celltower:
  file.write("%s\n" % row)
file.close()

# Append Vertical pattern now
file=open(fileout,'a')
for i in range(360,720):
	file.write("%s" % data[i])
file.close()