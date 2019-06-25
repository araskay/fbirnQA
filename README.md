# fbirnQA
This repository provides a set of tools to run the [fBIRN QA pipeline](https://www.nitrc.org/projects/bxh_xcede_tools/) on fMRI data and parse the output into a summary CSV file. Tools to run multiple instances of the pipeline in parallel on HPC clusters and/or on machines with multiple cores are included.

## Getting started
To maintain the sanity of the user processing large data sets of hundreds or thousands of files, all the tools in this toolbox are designed to work with fMRI *subjects files* - see the [fMRI pipeline](https://github.com/kayvanrad/fmri_pipeline) repository for details of the subjects files.

### Running the fBIRN QA pipeline on fMRI files
While the fMRI files can be processed sequentially using *run_fbirnQA.py*, it is strongly recommended to use the powerful parallel processing tools included in this package:
- For HPC clusters: use *prun_fbirnQA.py* to submit each instance of the pipeline to the job scheduler. This script takes care of the job submissions and merging the results inot a single subjects file in a seamless manner. This script currently support the SLURM scheduler.
- For running on local machines with multiple cores: user *prun_fbirnQA_localmachine.py* to run multiple instances of the pipeline in parallel. The user can specify how many cores to be used simultaneously. Once all the files are processed, the script merges the results into a single subjects file in a seamless manner.

### Parsing the output of the fMRI QA pipeline into a single CSV file
The fBRIN QA pipeline creates multiple outputs for each fMRI file. It is often desired to extract summary measures and save them in a single file for further analysis. This package includes a powerful tool, *parse_fbirnQA.py*, to parse the output of the pipeline into a single CSV file.

## Requirements
### Python version
The pipeline requires python 3 to run. However, if you really want to use python 2, you should be able to get it running in python 2 as well with some modifications. I recommend using [Anaconda Python 3](https://www.anaconda.com).

### Required libraries
To run the pipeline, the following libraries need to be installed: nibabel, nipype. The libraries can be installed using pip as follows:
```
pip install --user bibabel
pip install --user nipype
```
### The fBIRN QA pipeline
The [fBIRN QA pipeline](https://www.nitrc.org/projects/bxh_xcede_tools/) must be installed and accessible via the command line.

## Installation
Clone or download this repository to a directory of your choice. Make sure all the prerequisites are installed.

## Author
[Aras Kayvanrad](https://www.linkedin.com/in/kayvanrad/)

**Related repos:** [fmri_pipeline](https://github.com/kayvanrad/fmri_pipeline), [acf](https://github.com/kayvanrad/acf), [phantomQA](https://github.com/kayvanrad/phantomQA)
