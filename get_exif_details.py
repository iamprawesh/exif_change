import os
from PIL import Image
from PIL.ExifTags import TAGS
import piexif

# img_file = 'navrajedited.JPG'
img_file = 'navraj.JPG'

f = open("demofile2.txt", "a")

image = Image.open(img_file)
exif_dict = piexif.load(image.info['exif'])

exifdata = image.getexif()
exif = {}
# iterating over all EXIF data fields
# altitude = exif_dict['GPS'][piexif.GPSIFD.GPSAltitude]

for tag_id in exifdata:
    # get the tag name, instead of human unreadable tag id
    tag = TAGS.get(tag_id, tag_id)
    data = exifdata.get(tag_id)
    if isinstance(data, bytes):
        try:
            data = data.decode()
        except:
            continue
    print(f"{tag:35}: {data}")