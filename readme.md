# Python Geocoding Workflow

This repo contains four simple files that execute spaCy's [NER](https://spacy.io/api/entityrecognizer/) functionality on a group of files and use that output as an input for geocoding in 
[ArcGIS](https://developers.arcgis.com/rest/geocode/api-reference/overview-world-geocoding-service.htm)

## File Overview

The files consist of:

1. [arcGeocode.py](geocode.py): Runs spaCy and arcGIS, outputing a .json file with all the places (geopolitical entities) in your corpus and their lat/long coordinates.
2. [arcGeocode.sbatch](geocode.sbatch): Creates a batch job for arcGeocode.py.

## Usage instructions

1. Before doing anything, we need to navigate to the [ArcGIS site](https://developers.arcgis.com/rest/geocode/api-reference/overview-world-geocoding-service.htm), register with our Stanford email, and obtain an API key. You'll need to input this in the script later.

2. Once we have a key, we can ssh into sherlock by opening the terminal program and entering the syntax: 
```bash
ssh yourSUNetID@sherlock.stanford.edu
```

3. Once we are on Sherlock, we'll use a git command to copy the files we need from this github repo:
```bash
git clone https://github.com/bcritt1/geocoding_python.git
```

This will create a directory in your home space on Sherlock called "geocoding_python" with all the files in this repository.
![Repo Pull](https://github.com/bcritt1/H-S-Documentation/blob/main/images/repoPull.png)

4. Before we check it out, let's make a few directories to handle out outputs:
```bash
mkdir out err /scratch/users/$USER/outputs

Now you can move
```bash
cd geocoding_python
```
into your new directory.

5. There are a couple of necessary changes to the arcGeocode.py file:
	a. First, you'll need to change the ```corpusdir``` variable to your desired inputs, which should be plain txt files in the default configuration of the script. Other inputs are possible, but you'd need to tweak the code for this.
	b. Second, you must input your personal API key into the ```arcgis_api_key``` variable.

6. At this point, you should be able to run everything:
```bash
sbatch arcGeocode.sbatch
```
When it finishes running, you should see your output as a file called geocode.json in your outputs directory at /scratch/users/$USER/outputs/[^1].

## Code Overview

### arcGeocode.py

Fairly detailed in-line notes in the script itself, so check that out for more detail. Generally, the code reads in your corpus, tokenizes the corpus, and performs named entity recognition. One of the outputs of the last process is the 
labeling of places as Geopolitical Entities (GPEs). We then filter the data to retain only GPEs and feed those place names into Nominatim, which returns lat/long coordinates for those places.

### arcGeocode.sbatch

```bash
#!/usr/bin/bash
#SBATCH --job-name=arcode					# gives the job a descriptive name that slurm will use
#SBATCH --output=/home/users/%u/out/arcode.%j.out		# the filepath slurm will use for output files. I've configured this so it automatically inserts variables for your username (%u) and the job name (%j) above.
#SBATCH --error=/home/users/%u/err/arcode.%j.err		# the filepath slurm will use for error files. I've configured this so it automatically inserts variables for your username (%u) and the job name (%j) above.
#SBATCH -p hns							# the partition slurm will use for the job. Here it is hns (humanities and sciences), but you can use other partions (sh_part to see which you can access)
#SBATCH -c 4							# number of cores to use.
#SBATCH --mem=16GB						# memory to use. 16GB should be plenty, but if you're getting a memory error ('Killed' or 'OOM', you can increase
module load python/3.9.0
pip3 install spacy geopy
python3 arcGeocode.py
```

#### Notes

[^1]: Scratch systems offer very fast read/write speeds, so they're good for things like I/O. However, data on scratch is deleted every 60 days if not modified, so if you use scratch, you'll want to transfer results back to your home directory.
[^2]: There are a few likely culprits for failure here, just because everyone's data is different. First, spaCy places a limit on the length of inputs by default. I have upped this limit with the line in geocoding.py "nlp.max_length = 5000000". You can get a rough idea of the length of your input by running ```wc``` in your "corpus" directory. Something a little bigger than that number should be safe. Also depending on the size of your data, you may get a memory error, which can be adjusted in the "-mem" line of the geocode.sbatch file. There are some more notes on things you might want to tweak in the geocode.py file itself. As always, if you don't see your places.csv file once the process finishes, check the .out and .err files for your job. You can contact [me](mailto:bcritt@stanford.edu) if you can't debug from there.
