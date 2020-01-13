import hashlib
import glob

path = 'media/'
hashes = {}

files = glob.iglob(path + '**/*.*', recursive=True)


def get_hash(current_file):
    hash = hashlib.md5()
    hash.update(current_file)
    return hash.hexdigest()


for file in files:
    print("Currently processing: " + file)
    opened = open(file, 'rb')
    read = opened.read()
    current_hash = get_hash(read)
    # track all encounters
    if current_hash not in hashes:
        hashes[current_hash] = 1
    else:
        hashes[current_hash] += 1

for key, value in hashes.items():
    if value > 1:
        print(key + ": " + str(value))

print(len(hashes))