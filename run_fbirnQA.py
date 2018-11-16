#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 16:28:15 2018

@author: mkayvanrad
"""

import getopt, sys, subprocess, os
import workflow, fileutils
import xml.etree.ElementTree as et

def printhelp():
    print('Usage: run_fbrinQA.py --subjects <input subjects file> [--outputsubjects <output subjects file>]')
    
subjectsfile=''
outputsubjectsfile=''

# parse command-line arguments
try:
    (opts,args) = getopt.getopt(sys.argv[1:],'h',\
                                ['help','subjects=', 'outputsubjects='])
except getopt.GetoptError:
    printhelp()
    sys.exit()
for (opt,arg) in opts:
    if opt in ('-h', '--help'):
        printhelp()
        sys.exit()
    if opt in ('--subjects'):
        subjectsfile=arg
    if opt in ('--outputsubjects'):
        outputsubjectsfile=arg

if subjectsfile=='':
    printhelp()
    sys.exit()
    
subjects=workflow.getsubjects(subjectsfile)

subjcount=0
for subj in subjects:
    subjcount+=1
    for sess in subj.sessions:
        for run in sess.runs:
            print('processing',run.data.bold)
            print('subject',subjcount,'out of',len(subjects))
            (directory,namebase)=os.path.split(run.data.bold)
            namebase=fileutils.removext(namebase)
            opath=os.path.abspath(run.data.opath) # just to remove possible end slash (/) for consistency
            # wrap nifti image
            p=subprocess.Popen(['analyze2xcede',fileutils.addniigzext(run.data.bold),fileutils.removext(run.data.bold)+'_wrapped.xml']) # do not use analyze2bxh --xcede
            p.communicate()
            # nifti files do not contain frequencydirection in the header. add this info to the xml file. needed to calculate ghost measures
            tree = et.parse(fileutils.removext(run.data.bold)+'_wrapped.xml')
            root = tree.getroot()
            acq = root.find('{http://nbirn.net/Resources/Users/Applications/xcede/}acqProtocol')
            freqdim = et.Element('{http://nbirn.net/Resources/Users/Applications/xcede/}acqParam',{'name': 'frequencydirection', 'type': 'integer'})
            freqdim.text='1'
            acq.append(freqdim)
            tree.write(fileutils.removext(run.data.bold)+'_wrapped.xml')
            # run fbrin QA pipeline on the wrapped image
            # the fbirn pipeline has very specific requirements in terms of the output directory:
            # the directory should not exists,
            # but the pipeline cannot create more than one level of directory
            # so... the following is to go around the fbirn pipeline crazy directory handling... phew
            fileutils.createdir(opath+'/fBIRNQA')
            # if the directory already exists, create a new one
            count=0
            nb=namebase
            while os.path.exists(opath+'/fBIRNQA/'+namebase):
                count += 1
                namebase=nb+'_'+str(count)
            p=subprocess.Popen(['fmriqa_phantomqa.pl',fileutils.removext(run.data.bold)+'_wrapped.xml',opath+'/fBIRNQA/'+namebase])
            p.communicate()
            run.data.qa=opath+'/fBIRNQA/'+namebase+'/summaryQA.xml'
            
if len(outputsubjectsfile)>0:
    workflow.savesubjects(outputsubjectsfile,subjects)
