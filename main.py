import hashlib
import glob
import os

path = 'media/'
hashes = {}

files = glob.iglob(path + '**/*.*', recursive=True)


def get_hash(current_file):
    hash = hashlib.md5()
    hash.update(current_file)
    return hash.hexdigest()

def create_folder(folder):
    if not os.path.isdir(path + folder):
        os.mkdir(path + folder)

for file in files:
    print("Currently processing: " + file)
    opened = open(file, 'rb')
    read = opened.read()
    current_hash = get_hash(read)
    opened.close()
    # track all encounters
    if current_hash not in hashes:
        hashes[current_hash] = [1, [file]]
    else:
        hashes[current_hash][0] +=1
        hashes[current_hash][1].append(file)

# after getting all the hashes, move duplicates to a separate folder
create_folder('Duplicates')
create_folder('Duplicates/Keep')
create_folder('Duplicates/Delete')
for key, value in hashes.items():
    if value[0] > 1:
        print(key, value)
        duplicate_count = 1
        for duplicate in value[1]:
            fname = duplicate.split('\\')[-1]
            ftype = fname.split('.')[1] # possibly use MIME types later
            fname = fname.split('.')[0]
            if duplicate_count == 1:
                os.rename(duplicate, path + 'Duplicates/Keep/' + key + ' ' + str(duplicate_count) + '.'+ ftype)
            else:
                os.rename(duplicate, path + 'Duplicates/Delete/' + key + ' ' + str(duplicate_count) + '.' + ftype)
            duplicate_count += 1