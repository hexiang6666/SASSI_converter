# SASSI_converter
=============================

### Usage

SASSI converter can transfer [REAL ESSI](http://sokocalo.engr.ucdavis.edu/~jeremic/Real_ESSI_Simulator/) (UC Davis Earthquake-Soil-Structure-Interaction Simmulator) geometry and boundary condition to input files for [SASSI 2000](http://mtrassoc.com/mtrsassi/) for design of nuclear power plants (NPP)


### Installation

1) Get source from Github

```bash
https://github.com/hexiang6666/SASSI_converter.git
```

2) Copy or make links of [ESSI_preprocessor.sh] and [SASSI_converter.py] from Source code directory to current running directory.


3) make copied files executable

```bash
sudo chmod 777 ./ESSI_preprocessor.sh ./SASSI_converter.py
```

### Running

In order to run ###SASSI_convertor, you need to have RealESSI geometry and load files prepared (i.e. YOURMODELNAME_geometry.fei and YOURMODELNAME_load.fei). In order to transfer these files, simply run:


```bash
python SASSI_converter.py YOURMODELNAME
```


---
[UCD CompGeoMech](http://sokocalo.engr.ucdavis.edu/~jeremic/)

Created by: Hexiang Wang

Request for adding features on hexwang@ucdavis.edu


