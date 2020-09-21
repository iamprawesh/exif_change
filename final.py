import xlrd
import os
from PIL import Image
from PIL.ExifTags import TAGS
import datetime
# for converting to fraction number
from fractions import Fraction
import piexif
# for copying image
import shutil
# for generating random number
import random

path = os.getcwd()

# generating random number
foldername = "updated_exif{0}{1}".format(
    random.randint(1, 9), random.randint(1, 9))

new_dir_with_name = "{0}\{1}".format(path, foldername)

# creating file for storing updated images
try:
    os.mkdir(foldername)
except OSError:
    print("Creation of the directory {0} failed".format(new_dir_with_name))
else:
    print("Successfully created in '{0}'".format(new_dir_with_name))


def togdegree(value):
    abs_value = abs(value)
    deg = int(abs_value)
    t1 = (abs_value - deg) * 60
    min = int(t1)
    sec = round((t1 - min) * 60, 5)
    return [
        change_to_rational(deg),
        change_to_rational(min),
        change_to_rational(sec)
    ]


def change_to_rational(number):
    """convert a number to rantional
    Keyword arguments: number
    return: tuple like (1, 2), (numerator, denominator)
    """
    f = Fraction(str(number))
    return (f.numerator, f.denominator)


workbook = xlrd.open_workbook('datas.xlsx')
worksheet = workbook.sheet_by_name('Sheet1')
num_rows = worksheet.nrows - 1
curr_row = 0
# this is header of excel file
excel_headers = worksheet.row(0)
while curr_row < num_rows:
    curr_row += 1
    row = worksheet.row(curr_row)
    # getting file directory

    file_dir_with_name = row[0].value
    # copying image to new folder
    file_name = file_dir_with_name.split('\\')[-1]
    new_file_path = "{0}\\{1}".format(new_dir_with_name, file_name)

    print(file_dir_with_name)
    print(os.path.isfile(file_dir_with_name))

    if not os.path.isfile(file_dir_with_name):
        try:
            shutil.rmtree(new_dir_with_name)
            print(file_dir_with_name)
            print(
                f" INVALID FILE PATH at excel row number '{curr_row}' ! Make sure the excel file contains the valid file path ")
        except:
            print("Cannot delete the folder!")
        break
    try:
        shutil.copy(file_dir_with_name, new_file_path)
    except FileNotFoundError:
        print(
            f" Invalid dir name Image not found in that given directory'{file_dir_with_name}'")
        break

    for i in range(1, len(row)):
        for j in range(1, len(excel_headers)):
            if (i == j):
                exif_code = excel_headers[j].value.split('-')[1]
                exif_name = excel_headers[j].value.split('-')[0]
                try:
                    img = Image.open(new_file_path)
                except FileNotFoundError:
                    print(
                        f"Image not found in that given directory '{new_file_path}'")
                    break
                try:
                    # If the image already contains data, we only replace the relevant properties
                    exif_dict = piexif.load(img.info['exif'])
                    print(f"Exif load for file '{new_file_path}'' successful")
                except KeyError:
                    # If the image has no Exif data, we create the relevant properties
                    print(
                        f"No Exif data for file '{new_file_path}', creating Exif data instead..."
                    )
                    exif_dict = {}
                    exif_dict["0th"] = {}
                    exif_dict["Exif"] = {}
                if (len(exif_code) <= 3):
                    # for date change
                    if exif_code == '306':
                        exif_dict["Exif"][36868] = row[i].value.encode("utf-8")
                        exif_dict["Exif"][36867] = row[i].value.encode("utf-8")
                        exif_dict["0th"][306] = row[i].value.encode("utf-8")
                    # for GPS Locations
                    elif int(exif_code) <= 4:
                        if (exif_code == '1' or exif_code == '3'):
                            exif_dict["GPS"][int(exif_code)] = (
                                row[i].value).encode("utf-8")
                        else:
                            exif_dict["GPS"][int(exif_code)] = togdegree(
                                float(row[i].value))
                    else:
                        exif_dict["0th"][int(exif_code)] = (
                            row[i].value).encode("utf-8")
                        print(row[i].value)
                else:
                    if (len(row[i].value) != 0):
                        exif_dict["Exif"][int(exif_code)] = (
                            row[i].value).encode("utf-8")
                exif_bytes = piexif.dump(exif_dict)
                piexif.insert(exif_bytes, new_file_path)
                print(
                    f"Exif data replacement for file '{new_file_path}' successful"
                )
