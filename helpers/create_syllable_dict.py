import requests
import json
from tqdm import tqdm

syllables = {}
with open('output/unique_words.txt', 'r') as f:
    for word in tqdm(f.readlines(), desc="Fetching words"):
        word = word.strip()
        try:
            r = requests.get(f'https://api.datamuse.com/words?sp={word}&md=s&max=1')
            parsed = r.json()[0]
            syllables[word] = parsed['numSyllables']
        except Exception as e:
            # print("ERROR Could not get word:", word, e)
            syllables[word] = None

with open('output/syllable_dictionary.json', 'w') as f:
    f.write(json.dumps(syllables))
