#! /usr/bin/env python

# cube2xyz
# Extracts data from gaussian type .cube files and presents it as "x,y,z,measured_value"
# It can print output to terminal, file, or produce a plot directly with Mathplotlib.
# Cube file syntax: 
#   - 1st and 2nd lines are comment/free text
#   - 3rd line: Total no. of atoms, and x,y,z of the origin of the volume data
#   - 4th to 6th line: number of voxels (partition points) for each axis followed axis vectors#                      If the No. of voxels is >0 the units are in Bohr if <0 in Angstrom.
#   - 7th to No. of atoms: atom number, no. of electrons and xyz coordinates for each atom
#   - from there to the EOF: blocks of n voxels in xyz containing the value of the property
#                            measured in the cube file    
# 

import os, sys, argparse

version="0.1"

 
parser = argparse.ArgumentParser(description=""" cube2xyz can convert Gaussian type Cube files into "x y z value" columns, or project values on planes (slizes) or segments. Optionally, it can directly produce the plot for a faster visualization. \n """, epilog='\n Usage: cube2xyz -f out.spol.cube -o xyzspol.dat -x 3.1 -pl -A \n')
parser.add_argument('-f','--file_name', help="Name of cube file", required=True)
parser.add_argument('-o','--out_file', help="Name of the file to which print the output (otherwise printed to Standard Output).", required=False)
parser.add_argument('-pr','--print_range', help="Print the range of x,y or z values and exit.", required=False)
parser.add_argument('-x','--x_coord', help="Show only the values of x at this point.", required=False)
parser.add_argument('-y','--y_coord', help="Show only the values of y at this point.", required=False)
parser.add_argument('-z','--z_coord', help="Show only the values of z at this point.", required=False)
parser.add_argument('-pl','--plot', help="Plot graph using Mathplotlib.", required=False, action='store_true')
parser.add_argument('-A','--angstrom', help="Convert all distances to Angstrom. (def. a.u.)", required=False, action='store_true')
parser.add_argument('-no','--no_output', help="Do not produce any outupt.", required=False, action='store_true')
args = vars(parser.parse_args())
inpfile= args['file_name']


if args['angstrom']: # If "-A", convert distances to anstroms
 aa=1.0/0.5291772083
 p_label=" ($\AA$)"
else:
 aa=1.0
 p_label=" (a.u.)"


at_coord=[]
spacing_vec=[]
nline=0
values=[]
 # Read cube file and parse all data
for line in open(args['file_name'],"r"):
 nline+=1
 if nline==3:
  try:
   nat=int(line.split()[0]) 
   origin=[float(line.split()[1]),float(line.split()[2]),float(line.split()[3])]
  except:
   print "ERROR: non recognized cube format"
 elif nline >3 and nline <= 6:
  spacing_vec.append(line.split())
 elif nline > 6 and nline <= 6+nat:
  at_coord.append(line.split())
 elif nline > 5:
  if nline > 6+nat:
   for i in line.split():
    values.append(float(i)) 
   
print " "
def frange(x, y, jump):
  while x < y:
    yield x
    x += jump

idx=-1

if args['print_range']:
 print args['print_range']+" range:"
 if args['print_range'] == "x":
  for i in range(0,int(spacing_vec[0][0])):
    print i*float(spacing_vec[0][1])*aa
 if args['print_range'] == "y":
  for i in range(0,int(spacing_vec[1][0])):
    print i*float(spacing_vec[1][2])*aa
 if args['print_range'] == "z":
  for i in range(0,int(spacing_vec[2][0])):
    print i*float(spacing_vec[2][3])*aa
 sys.exit()


filter=""  # Create a filter for the values on a segment or plane
if args['x_coord']:
 filter=filter+ " x > "+str(float(args['x_coord'])-float(spacing_vec[0][1])+0.1) + " and x < " + str(float(args['x_coord'])+float(spacing_vec[0][1])-0.1) + " "
if args['y_coord']:
 if args['x_coord']:
   filter=filter+" and "
 filter=filter+ " y > "+str(float(args['y_coord'])-float(spacing_vec[1][2])+0.1) + " and y < " + str(float(args['y_coord'])+float(spacing_vec[0][1])-0.1) + " "
if args['z_coord']:
 if len(filter)> 3:
   filter=filter+" and "
 filter=filter+ " z > "+str(float(args['z_coord'])-float(spacing_vec[2][3])+0.1) + " and z < " + str(float(args['z_coord'])+float(spacing_vec[0][1])-0.1) + " "
if filter=="":
  filter="1==1"

 # Set parameter for type of plot
plttmp=[]
xyzs=""
if args['x_coord']:
 plttmp.append(args['x_coord'])
 xyzs=xyzs+"x"
if args['y_coord']:
 plttmp.append(args['y_coord'])
 xyzs=xyzs+"y"
if args['z_coord']:
 plttmp.append(args['z_coord'])
 xyzs=xyzs+"z"
plot_dim=4-len(plttmp)
print " Representing "+str(plot_dim)+"D data...", xyzs 


  #Print x,y,z,value data to stdout, file or not at all
data=[]
if args['out_file'] and not args['no_output']:  #if output file name is provided, print to file instead of STD out
 tmp=sys.stdout
 sys.stdout = open(args['out_file'],'w')
if args['no_output']:
 tmp=sys.stdout
 sys.stdout = open(os.devnull, 'w')

for i in range(0,int(spacing_vec[0][0])):
 for j in range(0,int(spacing_vec[1][0])):
  for k in range(0,int(spacing_vec[2][0])):
   idx+=1
   x,y,z= i*float(spacing_vec[0][1]),j*float(spacing_vec[1][2]),k*float(spacing_vec[2][3])
   if eval(filter):
    print x/aa,y/aa,z/aa, values[idx]
    data.append([x/aa,y/aa,z/aa, values[idx]])

if args['out_file'] or args['no_output']:
 sys.stdout.close()
 sys.stdout=tmp

ylabel="Cube magnitude"
axe_labels=["x","y","z"]
if args['plot']:
  try:
   from pylab import *
   print "pylab imported"
  except:
   print " ### ERROR: pylab not found. "
   sys.exit() 

  if plot_dim == 4:
   print "4D plot not implemented"
   sys.exit()

  if plot_dim == 3:
   var_axe1=list("xyz".replace(xyzs[0],""))[0]  
   var_axe2=list("xyz".replace(xyzs[0],""))[1]
   
   from mpl_toolkits.mplot3d.axes3d import Axes3D
   from matplotlib import cm
   import numpy as np
   #X, Y =np.meshgrid(zip(*data)[axe_labels.index(var_axe1)],zip(*data)[axe_labels.index(var_axe2)])
   X,Y=zip(*data)[axe_labels.index(var_axe1)],zip(*data)[axe_labels.index(var_axe2)]
   Z = zip(*data)[3]
   #print "max Z: ", max(Z)
   fig = plt.figure()
   ax = fig.gca(projection='3d')
   plt.hold(True)
   #surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
   surf = ax.plot_trisurf(X, Y, Z, cmap=cm.jet, linewidth=0.2)
   fig.colorbar(surf, shrink=0.5, aspect=5)
   ax.set_xlabel(var_axe1 + p_label)
   ax.set_ylabel(var_axe2 + p_label)
   ax.set_zlabel('Cube property')

   coord=[]
   for c in at_coord: # Format atomic coordinates for plotting
     coord.append([(float(c[2]))/aa,(float(c[3]))/aa,(float(c[4]))/aa])

   xc=zip(*coord)[axe_labels.index(var_axe1)]
   yc=zip(*coord)[axe_labels.index(var_axe2)]
   zc=[max(Z)+(max(Z)*0.2)]*len(coord)  # put the atoms slightly higher than the max value
    # projection of atoms centers above the graph
   ax.scatter(xc,yc,zc,s=150, c='b', marker='o',cmap=None, norm = None, edgecolors='c', lw=3.0) 
   #for i in coord:
   # print i[0], i[1], i[2]

 
  if plot_dim == 2:  # when 2 variables are fixed a 2D plot is produced
   var_axe= "xyz".replace(xyzs[0],"").replace(xyzs[1],"")
   var_idx=axe_labels.index(var_axe)
   plot(zip(*data)[var_idx], zip(*data)[3])
   plt.xlabel(var_axe + p_label)
   plt.ylabel("Cube property")
  
  plt.grid(True) 
  show()   





# 
# Writen by Julen Larrucea
# http://www.larrucea.eu 

#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.



