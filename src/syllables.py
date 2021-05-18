import json
import urllib.request as urllib2
def syllableCount(word):
	url='https://api.datamuse.com/words?md=s&max=1&sp=' + word
	data = json.load(urllib2.urlopen(url))
	if data[0]['word'] != word:
		print("API error")
	return data[0]['numSyllables']
	