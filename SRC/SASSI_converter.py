#********************************************************************************************************
# File:              SASSI_converter.py                                              
# Author:            hexiang                                     | Boris Jeremic,                       
# Date:              2017-08-10 11:37:31                         | University of California, Davis,95616*
# Description:       #############                               | California                           #
# Rev:               Version 1                                   | jeremic@ucdavis.edu                  #
# Email:             hexwang@ucdavis.edu                         | Computational Geomechanics Group     #
# * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  # 
#                           Last Modified time: 2017-03-16 22:29:55                                     #              
#  * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #        
# The copyright to the computer program(s) herein is the property of Hexiang Wang and Boris Jeremic     #
# The program(s) may be used and/or copied only with written permission of Hexiang Wang or in accordance#
# with the terms and conditions stipulated in the agreement/contract under which the program have been  #
# supplied.                                                                                             #
#*******************************************************************************************************#

#! /usr/bin/env python
import scipy as sp
import subprocess
import sys


######################## This is to calling preprocessor bash script ESSI_preprocessor to conduct text processing and get pure text file #####################################

bash_calling="./ESSI_preprocessor.sh " +  sys.argv[1]

subprocess.call(bash_calling, shell=True)

########################################################################################################################

node=sp.loadtxt("./node.temp")  ### node has 5 columns: 1 node ID, 3 coordinates and 1 number of dofs



############################## Currently SASSI only support 8 node brick element, conversion for 27 node brick element was not implemented #####################################

eight_solid_element=sp.loadtxt("./8nodebrickelement.temp")  ### eight_solid_element has 11 columns: 1 element ID, 1 elementTypeID (here for 8nodebrick is 8), 8 nodal IDs and 1 material tag


node_fixity=sp.zeros((node.shape[0],6));

node=sp.concatenate((node,node_fixity),axis=1)   #### By now node has 11 columns: first 5 columns plus 6 columns containing  fixity information

node_index={};

for x1 in xrange(0,node.shape[0]):
	node_index[node[x1,0]]= x1;       ### node_index serves as a map between node_ID and node_row_ID. Giving node_ID, node_index[node_ID] will return node_row_ID that contains the node information

with open("./fixity.temp") as f:
	content = f.readlines()

content = [x.strip() for x in content]

for x2 in xrange(0,len(content)):

# for x2 in xrange(0,3):   ## for debugging by Hexiang

	node_fixity_info = content[x2];

	node_fixity_info=node_fixity_info.split()

	node_ID = int(node_fixity_info[0]);
	
	node_row_ID = node_index[node_ID];
	
	fixity_size=len(node_fixity_info)-1;
	
	for x3 in xrange(0,fixity_size):
	
		fixity_code=int(node_fixity_info[x3+1]);

		# print fixity_code
	
		if fixity_code==1:
			
			node[node_row_ID,5]=1;       ### five-th column corresponds to ux
  
		if fixity_code==2:

			node[node_row_ID,6]=1;       ### six-th column corresponds to uy
				
		if fixity_code==3:

			node[node_row_ID,7]=1;       ### seven-th column corresponds to uz


# ############### 7,8 ,9 columns corresponds to  Rx, Ry, Rz, OR Ux, Uy, Uz. Bu now, has not been activated ##############################

		if fixity_code==4:
			
			node[node_row_ID,8]=1;       ### eigth-th column corresponds to ux
  
		if fixity_code==5:

			node[node_row_ID,9]=1;       ### nine-th column corresponds to uy
				
		if fixity_code==6:

			node[node_row_ID,10]=1;       ### ten-th column corresponds to uz

###########################################################################################################################################


f=open("./node.in","w+")

for x4 in xrange(0,node.shape[0]):

# for x4 in xrange(0,10):  ## for debugging by hexiang 

	if node[x4,0] > 99999:
		print " The node ID ", node[x4,0] ," exceeds the range of SASSI!!! At maximum the node ID can be 99999 \n";
	ID=format(int(node[x4,0]),'5d');
	x_translate=int(node[x4,5]);
	y_translate=int(node[x4,6]);
	z_translate=int(node[x4,7]);
	x_rotate = int(node[x4,8]);
	y_rotate = int(node[x4,9]);
	z_rotate = int(node[x4,10]);

	x_coord = format(node[x4,1],'10.4f')
	y_coord = format(node[x4,2],'10.4f')
	z_coord = format(node[x4,3],'10.4f')

	f.write("%s    %d    %d    %d    %d    %d    %d%s%s%s\n" %(ID, x_translate, y_translate, z_translate, x_rotate, y_rotate, z_rotate, x_coord,y_coord,z_coord)) 


f=open("./element.in","w+")

for x5 in xrange(0,eight_solid_element.shape[0]):
	
	if eight_solid_element[x5,0] > 99999: 

		print "The element ID ", element[x5,0], " exceeds the range of SASSI!!! At maximum the 8 node brick element ID can be 99999 \n";

	for x6 in xrange(0,8):

		if eight_solid_element[x5,x6+2] > 99999:
		
			print " The node ID ", eight_solid_element[x5,x6+2], " of element No ", element[x5,0] , " exceeds the range of SASSI!!! At maximum the node ID can be 99999 \n";

	ID=format(int(eight_solid_element[x5,0]),'5d');

########### SASSI and Real ESSI 8 node solid brick element nodal corresponding rule ###########################################################
#						 SASSI     				Real ESSI
# Node ID 				   1						8
# 						   2						5
# 						   3						6
# 						   4						7
# 						   5                        4
#						   6                        1
#						   7                        2
#						   8                        3
################################################################################################################################################ 

	nodal_ID_1 = format(int(eight_solid_element[x5,9]),'5d');

	nodal_ID_2 = format(int(eight_solid_element[x5,6]),'5d');

	nodal_ID_3 = format(int(eight_solid_element[x5,7]),'5d');	

	nodal_ID_4 = format(int(eight_solid_element[x5,8]),'5d');

	nodal_ID_5 = format(int(eight_solid_element[x5,5]),'5d');

	nodal_ID_6 = format(int(eight_solid_element[x5,2]),'5d');

	nodal_ID_7 = format(int(eight_solid_element[x5,3]),'5d');

	nodal_ID_8 = format(int(eight_solid_element[x5,4]),'5d');

	integration_order= int(2); 

	element_type = int(1);

	material_type = format(int(eight_solid_element[x5,10]),'5d');

	f.write("%s%s%s%s%s%s%s%s%s    %d    %d%s\n" %(ID, nodal_ID_1, nodal_ID_2, nodal_ID_3, nodal_ID_4, nodal_ID_5, nodal_ID_6, nodal_ID_7,nodal_ID_8, integration_order, element_type, material_type)) 


bash_calling="rm -rf ./*.temp"

subprocess.call(bash_calling, shell=True)


print "<<<<<<<<<<<<< Converting Details >>>>>>>>>>>>>>>>>>>>>\n"; 

print "Total number of nodes: ",  node.shape[0], "\n";

print "Total number of 8 node brick elements: ",  eight_solid_element.shape[0], "\n";

print "<<<<<<<<<<<< Happily Ending the Program >>>>>>>>>>>>>>>\n";

