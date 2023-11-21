#!/bin/bash
#you must create out/ and err/ directories in your home for this to work
#SBATCH --job-name=arcode
#SBATCH --output=/home/%u/out/arcode.%j.out
#SBATCH --error=/home/%u/err/arcode.%j.err
#SBATCH -p normal
#SBATCH -c 4
#SBATCH --mem=16GB

module load python/3.11.4
pip3 install spacy geopy
python3 arcGeocode.py 
