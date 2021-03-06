#!/usr/local/bin/python3

''' 
A simple wrapper for ffuf
Author: Andreas Wienes - Hack Like Demons - https://twitter.com/AndreasWienes

First draft: 2021-11-10
'''
# TODO: Add POST method

import argparse
import os
import urllib.parse

parser = argparse.ArgumentParser()
parser.add_argument('input_file', help='a file with URLs line by line as input for ffuf')
parser.add_argument('--options')
args = parser.parse_args()

user_agent = '"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"'
word_list = '~/hacking/tools/wordlists/hld_parameter_names.txt' # add your default wordlist here
input_file = args.input_file
options = args.options
if not options:
    options = ""
output_path = 'recon'
output_path_exist = os.path.exists(output_path)

print('\nFfufer - Batch parameter fuzzing based on ffuf\n')

if output_path_exist:
   print("Found existing folder 'recon'. All ouput files will be saved there.")   
else:
   os.makedirs(output_path)
   print("Created new folder 'recon'. All ouput files will be saved there.")

with open(input_file) as f:
    urls = [line.rstrip() for line in f]

for target_url in urls:    
    host_name = urllib.parse.urlparse(target_url).hostname.replace(".","_")
    path_name = urllib.parse.urlparse(target_url).path.replace("/","_")
    target_url = target_url + "\?FUZZ\\=1"
    output_file = f'ffuf_{host_name}-{path_name}'
    
    ffuf_command = f"ffuf -ac -c -t 50 -w {word_list} -H 'User-Agent: {user_agent}' -o {output_path}/{output_file}.html -of html {options} -u {target_url}"
    print(ffuf_command)
    os.system(ffuf_command)


