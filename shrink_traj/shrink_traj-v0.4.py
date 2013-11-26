#!/usr/bin/python

##  shrink_traj.py:
##   Python script for shrinking long and big molecular dynamics
##   "xyz" trajectory files into more easy-to-handle ones
##   v0.4 also can add unit cell information, which can be readen by Jmol
##
## By Julen Larrucea
## www.larrucea.eu

import os,sys
version=0.4

nat=0
linec=0 #line count
frame=[]
struc=0 #counter for structures in trajectory
step=3 #every how many frames do we print to output
trajfile="TRAJEC.xyz"
outfile="smallTRAJEC.xyz"
extrajmolcmd=""

if len(sys.argv)>1:
 for i in sys.argv:
  if i.startswith('-'):
   option=i.split('-')[1]
   if option=="f":
    trajfile= sys.argv[sys.argv.index('-f')+1]
   if option=="s":
    s= sys.argv[sys.argv.index('-s')+1]
    try:
     step=int(s)
    except:
     print "d must be an integer"
     sys.exit()
   if option=="o":
    outfile= sys.argv[sys.argv.index('-o')+1]

   if option=="cc":
     try: 
        cc= [sys.argv[sys.argv.index('-cc')+1],sys.argv[sys.argv.index('-cc')+2],sys.argv[sys.argv.index('-cc')+3]]
     except:
        print "Bad format: provide a, b and c cell vectors in Anstroms"
        sys.exit()

   if option=="cv":
     try: 
        cv= [sys.argv[sys.argv.index('-cv')+1],sys.argv[sys.argv.index('-cv')+2],sys.argv[sys.argv.index('-cv')+3],sys.argv[sys.argv.index('-cv')+4],sys.argv[sys.argv.index('-cv')+5],sys.argv[sys.argv.index('-cv')+6]]
     except:
        print "Bad format: provide a, b and c cell vectors in Anstroms"
        sys.exit()

   if option=="ej":
    extrajmolcmd= extrajmolcmd +";"+sys.argv[sys.argv.index('-ej')+1]

   if option=="v":
    print "shrink_traj.py v. " + float(version)
    sys.exit()
   if option=="h":
    print '''
  shrink_traj v '''+str(version)+''' help:
   -h: print this help
   -v: print version
   -f: name of trajectory file (def. TRAJEC.xyz)
   -s: step (every how many steps does it store a frame. Def. 3)
   -o: output name (def. smallTRAJEC.xyz)
  -cc: Cell Vectors for for Cubic Cell as: a b c (in Angstroms)
  -cv: Cell Vectors as: a b c alpha beta gamma (in Ansgtroms and degrees)
  -ej: Extra Jmol arguments (Def. "")

  Example: shrink_traj -s 50 -f TRAJEC.xyz -o smallTRAJEC.xyz -cv 5.50 5.50 9.4 90.0 90.0 90.0 -ej "background white; center"
'''
    sys.exit()


out=open(outfile,'w')
for line in open(trajfile,'r'):
  if line.strip().isdigit():
    nat=int(line.strip())
    linec=0
    struc+=1
    if len(frame)>0:
      print>>out,  "  ",nat
      if cc:
       #print>>out, "jmolscript: load \"\" {2 2 1} "
       print>>out, "jmolscript: load '' {1 1 1} unitcell {"+cc[0]+" "+cc[1]+" "+cc[2]+" 90 90 90} " + extrajmolcmd
      elif cv: 
       print>>out, "jmolscript: load '' {1 1 1} unitcell {"+cv[0]+" "+cv[1]+" "+cv[2]+" "+cv[3]+" "+cv[4]+" "+cv[5]+"} " + extrajmolcmd
      else: 
       print>>out,  "  stucture No.: ", struc-1
      for i in frame:
       print>>out, i[0],i[1],i[2],i[3]  
        
    frame=[]
  if float(struc)/float(step) == struc/step or struc==1:
    if linec>1:
     frame.append([line.split()[0],line.split()[1],line.split()[2],line.split()[3]])
    linec+=1
  

