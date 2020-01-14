import hashlib
import glob
import os
from PIL import Image

path = 'media/'
hashes = {}
errors = {}

files = glob.iglob(path + '**/*.*', recursive=True)


def get_hash(current_file):
    hash = hashlib.md5()
    hash.update(current_file)
    return hash.hexdigest()

def create_folder(folder):
    if not os.path.isdir(path + folder):
        os.mkdir(path + folder)


def get_timestamp(fname):
    try:
        image = Image.open(fname)
        image.verify()
        exif = image._getexif()
        exif_306 = exif.get(306) # Exif.Image.DateTime
        exif_36867 = exif.get(36867) # Exif.Photo.DateTimeOriginal
        exif_36868 = exif.get(36868) # Exif.Photo.DateTimeDigitized
        if exif_306 == exif_36867 == exif_36868:
            return exif_306
        else: # should return the one that is not None later
            return exif_36867
    except:
        pass


files_on_date = {}


for file in files:
    print("Currently processing: " + file)
    global new_name
    # rename all JPG files
    if file.lower().endswith('.jpg') or file.lower().endswith('.jpeg'):
        exif = get_timestamp(file).replace(' ', ':').replace('/', ':')
        year = exif.split(':')[0]
        month = exif.split(':')[1]
        day = exif.split(':')[2]
        hour = exif.split(':')[3]
        minute = exif.split(':')[4]
        second = exif.split(':')[5]
        ymd = year + month + day
        hrs = hour + minute + second
        ymdhrs = ymd + hrs
        # duplicate files would have creation timestamp, just rename duplicates until hashing confirms
        if ymdhrs not in files_on_date:
            files_on_date[ymdhrs] = 1
        else:
            files_on_date[ymdhrs] += 1
        if files_on_date == 1:
            duplicate_actual = ''
        else:
            duplicate_actual = str(files_on_date[ymdhrs])
        new_name = path + year + '-' + month + '-' + day + ' ' + hour + '_' + minute + '_' + second + duplicate_actual + '.jpg'
        os.rename(file, new_name)
    # else it's probably a MPEG, need to find EXIF equivalent for movies
    else:
        new_name = file

    opened = open(new_name, 'rb')
    read = opened.read()
    current_hash = get_hash(read)
    opened.close()
    # track all encounters
    if current_hash not in hashes:
        hashes[current_hash] = [1, [new_name]]
    else:
        hashes[current_hash][0] +=1
        hashes[current_hash][1].append(new_name)



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