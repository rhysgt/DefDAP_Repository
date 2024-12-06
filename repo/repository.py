import pooch
from pooch import Unzip
from defdap import hrdic, ebsd, experiment
import numpy as np
import yaml
import glob

def printYamls(folder):

    print('These are the yaml files in the yaml folder:\n')
    
    for file in glob.glob(folder + '/*.yml'):
        with open(file, 'r') as infile:
            data = yaml.load(infile, Loader=yaml.Loader)
    
            print('{:15} | {:30} | \033[1m {:30} \033[0m'.format(data['meta']['author'], data['meta']['name'], file))
            
def loadData(yaml_file, key=None):
    
    with open(yaml_file, 'r') as infile:
        yaml_dict = yaml.load(infile, Loader=yaml.Loader)

    # If zipped, use the Unzip processor
    if yaml_dict['meta']['zipped'] == True:
        fname = pooch.retrieve(
        url=yaml_dict['meta']['url'], 
        known_hash=yaml_dict['meta']['hash'], 
        progressbar = True,
        processor=Unzip())
    
        # Remove cache, hidden and checkpoint files from the list
        fname = [sa for sa in fname if not any(sb in sa for sb in ["_MACOSX", ".DS_Store", ".ipynb_checkpoints"])]
    
        # Get the folder name
        folder_name = fname[0][:fname[0].rfind("unzip")+6]
    
    else:
        folder_name = pooch.retrieve(
        url=yaml_dict['meta']['url'], 
        known_hash=yaml_dict['meta']['hash'], 
        progressbar = True)


    # If there is only one experiment key in the file, use that
    if len(yaml_dict['experiments']) == 1:
        key=list(yaml_dict['experiments'].keys())[0]
        
    elif len(yaml_dict['experiments']) > 1:
        # If there is more than one experiment key and one is not chose, throw error
        if key == None:
            raise Exception('Please choose an experiment from the file.\n \t\tOptions are: \n\t\t{}'.format(list(yaml_dict['experiments'].keys())))
        # If there is more than one experiment key and the chosen one does not exist, throw error
        if key not in yaml_dict['experiments'].keys():
            raise Exception('Key {} does not exist.\n \t\tOptions are: \n\t\t{}'.format(key, list(yaml_dict['experiments'].keys())))
        else:
            key=key
    
    
    exp = experiment.Experiment()
    
    items = yaml_dict['experiments'][key]
    
    # Get dic filenames
    if type(items['dic']) == str:
        dic_names = sorted(glob.glob(folder_name + items['dic']))
    elif type(items['dic']) == list:
        dic_names = [folder_name + i for i in items['dic']]
    
    # Load dic maps
    dic_frame = experiment.Frame()
    for dic_file in dic_names:
        hrdic.Map(dic_file, experiment=exp, frame=dic_frame)
    
    # Load ebsd map
    ebsd_frame = experiment.Frame()
    ebsd_map = ebsd.Map(folder_name + items['ebsd'], data_type=items['ebsd_type'], 
                        increment=exp.increments[0], frame=experiment.Frame())
    if items['ebsd_rotate'] == True:
        ebsd_map.rotate_data()
    
    # Homologous points
    dic_map = exp.increments[0].maps['hrdic']
    dic_map.frame.homog_points = items['dic_homog']
    ebsd_map.frame.homog_points = items['ebsd_homog']
    
    # Generate grain boundaries and grains
    ebsd_map.data.generate('grain_boundaries', misori_tol=items['ebsd_boundary_tolerance'])
    ebsd_map.data.generate('grains', min_grain_size=items['ebsd_min_grain_size'])
    
    
    
    for inc, dic_map in exp.iter_over_maps('hrdic'):
        dic_map.set_pattern(items['pattern'], items['pattern_scale'])
        dic_map.set_crop(left = items['dic_crop_left'], 
                   right = items['dic_crop_right'],
                  top = items['dic_crop_top'],
                  bottom = items['dic_crop_bottom'])
        dic_map.set_scale(items['dic_scale'])
    
        dic_map.link_ebsd_map(ebsd_map, transform_type = items['transform_type'])
    
        dic_map.data.generate('grains', min_grain_size=items['dic_min_grain_size'])

    return exp
