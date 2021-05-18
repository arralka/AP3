#Markov Chain Music Generation

**Requirements:**
* Python 3.7+
* Pandas
* Numpy

**Running**

Run using `python3 run.py`. The optional arguments for this script are as follows:

* `-artist` (str) : Name of the artist (as spelt under resources folder) - default is 'Linkin park'
* `-ngram` (int) : The ngram size (2 for bigram, 3 for trigram, etc) - default is 2
* `-lines` (int): The number of lines to generate - default is 8
* `-seed` (int) : The random seed for reproducibility - default is None
* `-verse` (str): Verse rhyming structure, each letter is a line, matching letters rhyme (except X, used for non-rhyming line)
* `-chorus` (str): Chorus rhyming structure, each letter is a line, matching letters rhyme (except X, used for non-rhyming line)

**Components**

There are three main modules: `Part1`, `Part2` and `Part3` - each of which as the names suggest correspond to their respective parts of the assignment.



