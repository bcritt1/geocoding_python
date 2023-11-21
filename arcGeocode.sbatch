#!/bin/bash
#SBATCH --job-name=arcode
#SBATCH --output=/home/users/%u/out/arcode.%j.out
#SBATCH --error=/home/users/%u/err/arcode.%j.err
#SBATCH -p hns
#SBATCH -c 4
#SBATCH --mem=16GB

module load python/3.9.0
pip3 install spacy geopy
python3 arcGeocode.py 
