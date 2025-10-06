This package contains yaml files, which each contain everything we need to load DIC/EBSD datasets from Zenodo, then link the DIC to the EBSD map using DefDAP, before displaying.

The yaml files contain
- Zenodo URL from which to dnwload
- Metadata (ie name and author)
- DIC map filename, crop, scale and homologous points
- EBSD map filename, type, rotation, grain boundary tolerance and homologous points
- DIC/EBSD transform type
- Pattern filename and scaling

These are parsed by included Python scripts, which means you load a variety of published DIC/EBSD datasets in one command.
