#*******************************************************************************************************#
# File:              ShellScript.tmpl                                              
# Author:            hexiang                                     | Boris Jeremic,                       #
# Date:              2017-08-10 11:57:06                         | University of California, Davis,95616#
# Description:       #############                               | California                           #
# Rev:               Version 1                                   | jeremic@ucdavis.edu                  #
# Email:             hexwang@ucdavis.edu                         | Computational Geomechanics Group     #
# * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  # 
#                           Last Modified time: 2017-08-11 15:12:41                                     #              
#  * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #         
# The copyright to the computer program(s) herein is the property of Hexiang Wang and Boris Jeremic     #
# The program(s) may be used and/or copied only with written permission of Hexiang Wang or in accordance# 
# with the terms and conditions stipulated in the agreement/contract under which the program have been  #
# supplied.                                                                                             #
#*******************************************************************************************************#

#!/bin/bash
echo "<<<<<<<<<<<<< SASSI converter launching >>>>>>>>>>>>>>>>>>"
echo ""

model_name=$1

geometry_file_name=$model_name"_geometry.fei"

load_file_name=$model_name"_load.fei"

rm -f node.include
sed -n '/[ ]*add[ ]*node/p' $geometry_file_name  >node.include
sed 's/[a-df-zA-DF-Z#(),;*]/ /g' node.include >node.4
sed 's/[\t ]e/ /g' node.4 > node.include 
rm node.4

rm -f 8nodebrickelement.include
sed -n '/[ ]*add[ ]*element[ #A_Za-z0-9]*8NodeBrick/p'  $geometry_file_name >8nodebrickelement.include
sed 's/[a-zA-Z#(),;_=*]/ /g' 8nodebrickelement.include >8nodebrickelement.4
mv 8nodebrickelement.4 8nodebrickelement.include

rm -f 27nodebrickelement.include
sed -n '/[ ]*add[ ]*element[ #A_Za-z0-9]*27NodeBrick/p'  $geometry_file_name  >27nodebrickelement.include
sed 's/[a-zA-Z#(),;_=*]/ /g' 27nodebrickelement.include >27nodebrickelement.4
mv 27nodebrickelement.4 27nodebrickelement.include



rm -f fixity.include
sed -n '/[ ]*fix[ ]*node[ #A_Za-z0-9]*dofs/p'  $load_file_name  > fixity.include

# currently just for the fixity of 3-dofs node
sed 's/ux/1/g' fixity.include >fixity.4
sed 's/uy/2/g' fixity.4 >fixity.include
sed 's/uz/3/g' fixity.include >fixity.4

sed 's/[a-zA-Z#(),;_=*]/ /g' fixity.4 >fixity.include

rm fixity.4 


touch ./ElementTypeTag.temp
mv ./node.include ./node.temp
mv ./8nodebrickelement.include ./8nodebrickelement.temp
mv ./27nodebrickelement.include ./27nodebrickelement.temp
mv ./fixity.include ./fixity.temp



if [ -s "./8nodebrickelement.temp" ]
then
	echo "1" >> ./ElementTypeTag.temp
else
	echo "0" >> ./ElementTypeTag.temp 
	rm ./8nodebrickelement.temp
fi

if [ -s "./27nodebrickelement.temp" ]
then
	echo "1" >> ./ElementTypeTag.temp
else
	echo "0" >> ./ElementTypeTag.temp 
	rm ./27nodebrickelement.temp
fi

