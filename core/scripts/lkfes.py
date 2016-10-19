#!/usr/bin/python3
#-*-coding:utf-8-*-

import json
import sys
import os


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def print_help():
	print("TODO : print_help")

def shell_command(command, error_str='', print_on_error=True, exit_on_error=True) :
    ret = os.system(command)
    if ret :   
        if print_on_error :
            if error_str :
                eprint(error_str)
            else :   
                eprint("failed : "+command)
        if exit_on_error :
            exit(1)
    return ret 


if len(sys.argv) < 1 :
	eprint("faild : missing required argument.")
	print_help()
	exit(1)


abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname+'/../..') #project root dir

eval_fname = sys.argv[1]
conf_path = 'core/scripts/feature_eval.conf' 
#TODO conf_path를 실행 디렉토리랑 상관없이 읽을 수 있도록 해야함.




#parsing argument
pre_arg = ''
for arg in sys.argv :
    if pre_arg == '--conf_path' :
        conf_path = arg 
    pre_arg = arg 

features = ''
try:
	feconf_file = open(conf_path, 'r')
	features = json.load(feconf_file)
	feconf_file.close()
except ValueError :
	eprint(conf_path+' is not valid.')
	exit(1)
except IOError:
	eprint(conf_path+' is not found.')
	exit(1)

try:
	feature = features[eval_fname]
except KeyError :
	eprint(eval_fname+" information does not exists in %s." % conf_path)

eval_script = feature['evaluation_script']
img_cnt = feature['image_cnt']
feature_imgs = feature['images']

scripts_path = 'core/scripts/'
kfe_path = scripts_path+'kfeature-eval.sh'

for i in range(img_cnt):
	version = feature_imgs[i]['version']
	configs = feature_imgs[i]['config']
	configs_string = ''
	for k, v in configs.items():
		configs_string += k+'='+v+','
	configs_string = configs_string[:-1]
	print(kfe_path+' -v '+ feature_imgs[i]['version']+' -c '+configs_string + ' -e '+eval_fname+'i')
	shell_command(kfe_path+' -v '+version+' -c '+configs_string+' -e '+eval_fname+'i'+' -s '+eval_script)






