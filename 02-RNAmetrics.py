import os, sys, numpy as np, subprocess as sp

maindirectory=sys.argv[1]
outdirectory=sys.argv[2]
commandprefix=sys.argv[3]


files=[x.split('_Aligned')[0] for x in os.listdir(maindirectory) if x.endswith('_Aligned.sortedByCoord.out.bam')]
refflat="/work/schnablelab/nikees/AlternateSplicing/reference/Zm-B73-REFERENCE-NAM-5.0_Zm00001eb.1.reflat.txt"


interval=list(np.arange(0,len(files),2))

interval.append(len(files))

print(interval)

for i, a in enumerate(interval[:-1]):
    slurm=open(f'/work/schnablelab/nikees/AlternateSplicing/PythonSlurms/{commandprefix}_{i}.slurm','w')
    slurm.write('#!/bin/sh\n' +
		    '#SBATCH --time=7-00:00:00\n' +
            '#SBATCH --mem=50G\n' +
            f'#SBATCH --job-name={commandprefix}_{i}\n' +
            f'#SBATCH --error=/work/schnablelab/nikees/AlternateSplicing/logs/{commandprefix}_{i}.err\n' +
            f'#SBATCH --output=/work/schnablelab/nikees/AlternateSplicing/logs/{commandprefix}_{i}.out\n' +
            '#SBATCH --partition=schnablelab,jclarke,batch,guest\n' +
	    	'module load picard\n')
    
    for asp in files[a:interval[i+1]]:

        inputfile=f"{maindirectory}/{asp}_Aligned.sortedByCoord.out.bam"
        outputfile=f"{outdirectory}/{asp}.csv"

        picardscript=f"picard CollectRnaSeqMetrics I={inputfile} O={outputfile} REF_FLAT={refflat} STRAND_SPECIFICITY=NONE"

        slurm.write(f"{picardscript}\n")

    slurm.close()
    sp.call(f'sbatch /work/schnablelab/nikees/AlternateSplicing/PythonSlurms/{commandprefix}_{i}.slurm', shell=True)




