#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 11:10:17 2018

@author: mkayvanrad
"""

import xml.etree.ElementTree as et
import getopt, sys, os
import workflow, fileutils


def parse_xml(xmlfile):
    tree = et.parse(xmlfile)
    root = tree.getroot()
    d = dict()
    for e in root[0][1].findall('{http://www.xcede.org/xcede-2}observation'):
        d[e.attrib['name']] = e.text
    return(d)
   
def printhelp():
    print('Parse the output of the fBIRN QA pipeline into a CSV file.')
    print('Usage: parse_fbrinQA.py --subjects <input subjects file> --output <output csv file>')

subjectsfile=''
outputfile=''

# parse command-line arguments
try:
    (opts,args) = getopt.getopt(sys.argv[1:],'h',\
                                ['help','subjects=', 'output='])
except getopt.GetoptError:
    printhelp()
    sys.exit()
for (opt,arg) in opts:
    if opt in ('-h', '--help'):
        printhelp()
        sys.exit()
    if opt in ('--subjects'):
        subjectsfile=arg
    if opt in ('--output'):
        outputfile=arg

if subjectsfile=='' or outputfile=='':
    printhelp()
    sys.exit()


qa_fields=['origdimensions', 'origspacing', 'origgap', 'slice', 'timepoints', 'roiSize', 'scanner', 'psdname', 'diffimagefile', 'meanimagefile', 'stdimagefile', 'sfnrimagefile', 'mean', 'SNR', 'SFNR', 'std', 'percentFluc', 'drift', 'driftfit', 'rdc', 'minCMassX', 'minCMassY', 'minCMassZ', 'maxCMassX', 'maxCMassY', 'maxCMassZ', 'meanCMassX', 'meanCMassY', 'meanCMassZ', 'dispCMassX', 'dispCMassY', 'dispCMassZ', 'driftCMassX', 'driftCMassY', 'driftCMassZ', 'minFWHMX', 'minFWHMY', 'minFWHMZ', 'maxFWHMX', 'maxFWHMY', 'maxFWHMZ', 'meanFWHMX', 'meanFWHMY', 'meanFWHMZ','meanGhost','meanBrightGhost']

subjects=workflow.getsubjects(subjectsfile)

f=open(outputfile,'w')

# write csv header
f.write('sessionID')
for field in qa_fields:
    f.write(',')
    f.write(field)
f.write('\n')

for subj in subjects:
    for sess in subj.sessions:
        for run in sess.runs:
            (directory,namebase)=os.path.split(run.data.bold)
            namebase=fileutils.removext(namebase)
            if os.path.exists(run.data.qa):
                print(namebase)
                d = parse_xml(run.data.qa)
                # write data to csv file
                f.write(namebase)
                for field in qa_fields:
                    if (field in d.keys()) and (d[field] is not None):
                        f.write(',')
                        f.write(d[field])
                    else:
                        f.write(',')
                f.write('\n')
            else:
                print(namebase,'(ERROR) QA file does not exists. Moving on.')
            
f.close()
            
