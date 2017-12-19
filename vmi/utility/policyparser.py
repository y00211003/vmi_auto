'''
Created on 2012-11-27

@author: joshua_liu
'''
import os.path
import platform
import subprocess

def parse_firewall_policy(unzip_dir = '.',
                          output_file = 'firewall_policy.ini'):
    unzip_dir = os.path.abspath(unzip_dir)
    if not os.path.isdir(unzip_dir):
        raise IOError('Not a directory ' + unzip_dir)
    if not os.path.isabs(output_file):
        output_file = os.path.join(unzip_dir, output_file)
    tools_dir = os.path.join(os.path.dirname(__file__), 'tools')
    if platform.system() == 'Windows':
        parser_bin = os.path.join(tools_dir, 'firewall_policy_parse.exe')
    elif platform.system() == 'Linux':
        parser_bin = os.path.join(tools_dir, 'firewall_policy_parse')
    else:
        raise RuntimeError('Not supported platform: ' + platform.system())
    return subprocess.call([parser_bin, unzip_dir, output_file])

def parse_data_security_policy(original_file = 'policy.mse',
                               output_file = 'dataSecurityPolicy.xml'):
    original_file = os.path.abspath(original_file)
    if not os.path.isfile(original_file):
        raise IOError('Not a file ' + original_file)
    if not os.path.isabs(output_file):
        output_file = os.path.join(os.path.dirname(original_file), output_file)
    tools_dir = os.path.join(os.path.dirname(__file__), 'tools')
    if platform.system() == 'Windows':
        parser_bin = os.path.join(tools_dir, 'DSParsePolicy', 'DeMSE.exe')
    else:
        raise RuntimeError('Not supported platform: ' + platform.system())
    return subprocess.call([parser_bin, original_file, output_file])

if __name__ == '__main__':
    pass