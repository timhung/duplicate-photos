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
        hashes[current_hash] = [1, [file]]
    else:
        hashes[current_hash][0] +=1
        hashes[current_hash][1].append(file)

# after getting all the hashes, move duplicates to a separate folder
for key, value in hashes.items():
    if value[0] > 1:
        print(key, value)

print(len(hashes))