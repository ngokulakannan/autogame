import json,os

def get_config(path='config.json'):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    fp = open(os.path.join( dir_path, path),'r')
    conf=json.load(fp)
    fp.close()
    return conf

# c=get_config()
# print(tuple(c['window_dim']))
