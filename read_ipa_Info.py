#!/usr/bin/env python3
#-*-coding : utf-8 -*-
import os
import sys
import time
from biplist import *
import zipfile
import json
import hashlib

if len(sys.argv) == 1:
    print('error: Please input the Path of ipa!')
    exit()

arg = sys.argv[1]




def read_plist():

    print('Loading...')
    
    # read zip
    f = zipfile.ZipFile(arg,'r')

    # unzip zipfile
    for file in f.namelist():
        f.extract(file,'.')

    # unzip done
    f.close()

    # get Bundle path
    reslutA = os.popen('pwd')
    pathB = reslutA.read()
    completePath = pathB + '/' + 'Payload'
    completePath = completePath.replace("\n","")
    reslutB = os.popen('ls ' + completePath)
    pathB = reslutB.read()
    completePath = completePath + '/' + pathB
    completePath = completePath.replace("\n","")



    # get macho path
    macho_path = completePath + '/' + pathB[:-5]

    # get Info.plist path
    plist_path = completePath + '/' + 'Info.plist'

    # print the version
    plist = readPlist(plist_path)
    print('\n')
    print(pathB[:-5] + '\'s version:')
    dict = plist['CFBundleShortVersionString']
    print(json.dumps(dict, indent=1))
    print('\n')

    # print the ipa MD5
    print(arg.split('/')[-1] + '\'s MD5:')
    MD5Str = os.popen('MD5 ' + arg)
    md5str = MD5Str.read();
    md5str = md5str.split('=')[1]
    print(arg.split('/')[-1] + md5str)
    # 7048de991a74359c70b221879fefcfc6

    # print the ATS
    print('\n')
    dict = plist['NSAppTransportSecurity']
    print(json.dumps(dict, indent=1))
    print('\n')


    # print the entitlement
    os.system('ldid -e ' + macho_path)

#     # open IDA
#     os.system('open /Applications/IDA\ Pro\ 7.0/ida64.app')


read_plist()

