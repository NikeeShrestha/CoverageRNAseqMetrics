#!/bin/bash
#SBATCH --mem-per-cpu=30G
#SBATCH --time=7:00:00
#SBATCH --partition=schnablelab,jclarke,batch,guest
#SBATCH --output=/work/schnablelab/nikees/AlternateSplicing/logs/%x_%a.out
#SBATCH --error=/work/schnablelab/nikees/AlternateSplicing/logs/%x_%a.err
#SBATCH --mail-type=ALL
#SBATCH --mail-user=nshrestha5@unl.edu

ml python/3.8

python /work/schnablelab/nikees/AlternateSplicing/scripts/02-RNAmetrics.py /work/schnablelab/nikees/AlternateSplicing/Alignedreadsgtf_exon /work/schnablelab/nikees/AlternateSplicing/RNAmetrics "RNAmrtrics"