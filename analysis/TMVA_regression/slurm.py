import subprocess
import argparse
import os

# SLURM script template
slurm_script_template = '''#!/bin/bash
#SBATCH --job-name={sample}
#SBATCH --output={log_dir}{sample}.out
#SBATCH --error={log_dir}{sample}.err
#SBATCH --time=15:00:00
#SBATCH --mem=2GB
#SBATCH --partition=submit

source ~/.bashrc
conda activate myenv
cd {work_dir}
{cmd}
'''

parser = argparse.ArgumentParser(description="Famous Submitter")
parser.add_argument("-i", "--input", type=str, required=True, help="Use specific input file (.txt) of jobs.")
parser.add_argument("--minIndex", type=int, default=0, help="Index of the first command (default: 0).")
parser.add_argument("--maxIndex", type=int, default=-1, help="Index of the last command (default: len(jobs)).")
options = parser.parse_args()

# Set up where you're gonna work
work_dir = os.getcwd()
log_dir = '/data/submit/pdmonte/TMVA_models/logsVars/'
if not os.path.isdir(log_dir):
    os.mkdir(log_dir)

# Read jobs from input file
with open(options.input, 'r') as f:
    jobs = f.read().splitlines()

if(options.maxIndex == -1):
    options.maxIndex = len(jobs)
# Loop over samples
for i, job in enumerate(jobs[options.minIndex:options.maxIndex]):
    sample, cmd = job.split(":")
    print(i, sample)
    
    # Generate the SLURM script content
    slurm_script_content = slurm_script_template.format(log_dir=log_dir, work_dir=work_dir, cmd=cmd, sample=sample)   

    # Write the SLURM script to a file
    slurm_script_file = f'{log_dir}slurm_{sample}.sh'
    with open(slurm_script_file, 'w') as f:
        f.write(slurm_script_content)

    # Submit the SLURM job
    subprocess.run(['sbatch', slurm_script_file])
