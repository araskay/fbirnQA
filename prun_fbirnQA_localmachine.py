#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys,getopt,subprocess,os
import workflow

def printhelp():
    print('Run multiple instances of the fBIRN QA pipeline in parallel '+
    'on a local machine with multiple CPU cores.')
    p=subprocess.Popen(['run_fbirnQA.py','-h'])
    p.communicate()
    print('---------------------------------')
    print('Additional job scheduler options:')
    print('[--numpar <number of parallel jobs = 16>]')

subjectsfile=''
outputsubjectsfile=''
numpar=16

# parse command-line arguments
try:
    (opts,args) = getopt.getopt(sys.argv[1:],'h',\
                                ['help','subjects=', 'outputsubjects=','numpar='])
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
    elif opt in ('--numpar'):
        numpar=int(arg)

if subjectsfile=='':
    printhelp()
    sys.exit()

subjects=workflow.getsubjects(subjectsfile)

base_command = 'run_fbirnQA.py'

count=0
proccount=0
processes = []

# get input file name to use for naming temporary files
(directory,filename)=os.path.split(subjectsfile)

for s in subjects:
    # first create individual subjects files and job bash scripts to be
    # submitted to the job manager
    count+=1
    proccount+=1

    subject_fname = '.temp_run_fbirnQA_subj_'+filename+str(count)+'.txt'
    
    command=[]

    workflow.savesubjects(subject_fname,[s],append=False)

    outputfile='.temp_run_fbirnQA_job_localmachine_'+filename+str(count)+'.o'
    errorfile='.temp_run_fbirnQA_job_localmachine_'+filename+str(count)+'.e'

    f_o = open(outputfile, 'w')
    f_e = open(errorfile, 'w')

    command.append(base_command)
    #Just re-use the arguments given here
    pipe_args = sys.argv[1:]

    pipe_args[pipe_args.index('--subjects')+1] = subject_fname

    if '--numpar' in pipe_args:
        del pipe_args[pipe_args.index('--numpar')+1]
        del pipe_args[pipe_args.index('--numpar')]

    command = command+ pipe_args
    
    # now submit job
    print('Running',' '.join(command))
    p=subprocess.Popen(command,stdout=f_o,stderr=f_e)
    processes.append(p)

    if proccount==numpar:
        for p in processes:
            p.wait()
        proccount=0
        processes=[]
        print('Total of',count,'jobs done')

for p in processes:
    p.wait()  
