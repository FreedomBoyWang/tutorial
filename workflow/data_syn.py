
# %%
import json
import pandas as pd
import os
import re
import time
import argparse

def get_valid_variable_name(name):
    pattern = re.compile(r'^[a-zA-Z_\u4e00-\u9fa5]\w{0,254}$')
    return name if pattern.match(name) is not None else 'var_{:3.3f}'.format(time.time()%100).replace('.','_')
if __name__=='__main__':
    # %%
    parser = argparse.ArgumentParser()
    parser.add_argument('-c',"--config_path", help="path",default='./config/reader_config.json')
    args = parser.parse_args()
    a=os.listdir()
    json_path=args.config_path
    with open(json_path) as f:
        config_json=json.load(f)
    workspace_folder=config_json['configuration']['workspace_folder']
    select_template=config_json['configuration']['select_template']
    file_ext=config_json['configuration']['file_ext']

    # %%
    para=''
    for config in config_json['templates']:
        if config['name']==select_template:
            for k,v in config['parameters'].items():
                if isinstance(v,str):
                    para+=',{}=\'{}\''.format(k,v)
                else:
                    para+=',{}={}'.format(k,str(v))
            break

    # %%
    file_list=os.listdir(workspace_folder)
    keep_vars=['keep_vars']
    for filename in file_list:
        f,ext=os.path.splitext(filename)
        if ext not in file_ext:
            continue
        varname = get_valid_variable_name(f)
        
        exec(f"{varname}=pd.read_csv(r'{os.path.join(workspace_folder,filename)}'{para})")
        keep_vars.append(varname)
        print(varname,'\t',filename)
    for var_name in dir():
        if var_name not in keep_vars and var_name[0]!='_':
            del globals()[var_name]
    del keep_vars
    del var_name


