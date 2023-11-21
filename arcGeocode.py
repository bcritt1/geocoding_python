from geopy.geocoders import ArcGIS
from geopy.exc import GeocoderAuthenticationFailure
import pandas as pd
import os
import spacy
import json

# Read in corpus from scratch
user = os.getenv('USER')
corpusdir = '/farmshare/learning/data/emerson/'
corpus = []
for infile in os.listdir(corpusdir):
    with open(corpusdir+infile, errors='ignore') as fin:
        corpus.append(fin.read())

# Load language model from spacy. This can be changed to other languages. See https://spacy.io/usage/models/
nlp = spacy.load("en_core_web_sm")
# May need to increase length for large corpora. len(corpus) in python to find length.
nlp.max_length = 5000000
# Convert corpus to string to make spacy happy
sorpus = str(corpus)
# Perform nlp on sorpus
doc = nlp(sorpus)
# Label entities types in doc
ner_output = []
for token in doc:
    ner_output.append(token.text + token.ent_type_)
# Convert to dataframe to clean
df = pd.DataFrame(ner_output)
# Retain only entities labeled as geopolitical entities. Can change string to retain people or other types.
places = df.loc[df[0].str.contains("GPE")]
places[0] = places[0].str.replace('GPE','')
print(places)
place_names=list(places[0])

def geocode_places(place_names, api_key):
    geolocator = ArcGIS()

    # Set the API key using an exception handler
    try:
        geolocator.api_key = api_key
    except GeocoderAuthenticationFailure as e:
        print(f"Authentication failed: {e}")
        return []

    geocoded_results = []
    for place in place_names:
        location = geolocator.geocode(place)
        if location:
            geocoded_results.append({
                'place_name': place,
                'latitude': location.latitude,
                'longitude': location.longitude,
                'address': location.address
            })
        else:
            geocoded_results.append({
                'place_name': place,
                'latitude': None,
                'longitude': None,
                'address': None
            })

    return geocoded_results

# Replace 'YOUR_API_KEY' with your actual ArcGIS API key
arcgis_api_key = 'YOUR_API_KEY'

geocoded_results = geocode_places(place_names, arcgis_api_key)

# Output JSON file path with user-specific directory
output_json_file = '/scratch/users/{}/outputs/geocode.json'.format(user)

with open(output_json_file, 'w') as json_file:
    json.dump(geocoded_results, json_file, indent=2)
