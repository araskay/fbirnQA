#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys,getopt,subprocess,os
import workflow

def printhelp():
    p=subprocess.Popen(['run_fbirnQA.py','-h'])
    p.communicate()


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

base_command = 'run_fbirnQA.py'

count=0

# get input file name to use for naming temporary files
(directory,filename)=os.path.split(subjectsfile)

for s in subjects:
    # first create individual subjects files and job bash scripts to be
    # submitted to the job manager
    count+=1
    subject_fname = '.temp_run_fbirnQA_subj_'+filename+str(count)+'.txt'
    qbatch_fname = '.temp_run_fbirnQA_job_'+filename+str(count)+'.sh'
    qbatch_file = open(qbatch_fname, 'w')
    
    workflow.savesubjects(subject_fname,[s],append=False)

    # write the header stuff
    qbatch_file.write('#!/bin/bash\n\n')
    qbatch_file.write('#$ -o .temp_run_fbirnQA_job_'+filename+str(count)+'.o'+'\n')
    qbatch_file.write('#$ -e .temp_run_fbirnQA_job_'+filename+str(count)+'.e'+'\n\n')
                      
    qbatch_file.write(base_command + ' ')
    #Just re-use the arguments given here
    pipe_args = sys.argv[1:]
    pipe_args[pipe_args.index('--subjects')+1] = subject_fname
    command_str  = ' '.join(pipe_args)
    qbatch_file.write(command_str)
    qbatch_file.write('\n')
    
    qbatch_file.close()
    
    # now submit job
    p=subprocess.Popen(['qsub',qbatch_fname])
    p.communicate()            

