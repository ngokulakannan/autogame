import json,os

def get_config(path='config.json'):
    '''
    Parse configuration json and return configuration dictionary

    Parameters
    ----------
    path - str
        path to configuration file
    '''
    dir_path = os.path.dirname(os.path.realpath(__file__))
    fp = open(os.path.join( dir_path, path),'r')
    conf=json.load(fp)
    fp.close()
    return conf


