This package contains yaml files, which each contain everything we need to load and link DIC/EBSD datasets, including:
- Zenodo URL
- Metadata like name and author
- DIC map filename, crop, scale and homologous points
- EBSD map filename, type, rotation, grain boundary tolerance and homologous points
- DIC/EBSD transform type
- Pattern filename and scaling

These are parsed by included Python scripts, which means you load a variety of published DIC/EBSD datasets in one line.
