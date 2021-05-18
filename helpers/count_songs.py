import os

counts = {}

for letter in os.listdir('resources'):
    for artist in os.listdir(f'resources/{letter}'):
        count = 0

        for album in os.listdir(f'resources/{letter}/{artist}'):
            for song in os.listdir(f'resources/{letter}/{artist}/{album}'):
                count+=1

        counts[artist] = count

results = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))
print(results)