#!/usr/bin/env python3
#-*-coding : utf-8 -*-
import os
import sys
import time
from biplist import *
import zipfile
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString
import xmltodict

if len(sys.argv) == 1:
    print('error: Please input absolute Path of the ipa!')
    exit()

arg = sys.argv[1]

if not ('/' in arg):
    print('error: Please input absolute Path of the ipa!')
    exit()

def read_plist():

    print('Loading...')
    
    backArg = arg[::-1]
    num = backArg.index('/')
    ipa_name = backArg[0:num]
    ipa_name = ipa_name[::-1]
    ipa_name = ipa_name[:ipa_name.index('.')]

    ipa_path = backArg[backArg.index('/'):]
    ipa_path = ipa_path[1:]
    ipa_path = ipa_path[::-1]

    f = zipfile.ZipFile(arg,'r')

    for file in f.namelist():
        f.extract(file,'.')

    plist_path = '%s/Payload/%s.app/Info.plist' % (ipa_path, ipa_name)

    # print the ATS
    plist = readPlist(plist_path)
#    print (plist['NSAppTransportSecurity'])

    print('\n')
    dict = plist['NSAppTransportSecurity']
    xml = xmltodict.unparse(dict,encoding='utf-8')
    print(xml)
    print('\n')

    macho_path = '%s/Payload/%s.app/%s' % (ipa_path, ipa_name, ipa_name)

    # print the entitlement
    print(ipa_name + '\'s entitlement')
    os.system('ldid -e ' + macho_path)

read_plist()

