import os
import zipfile
import argparse
from glob import glob

def try_extract_multiple_files(path):
    # File Structure:
    # - dir
    # -- xxx.zip

    # Get all files under this dir:
    file_container = glob(path)

    # Used to store stat:
    extract_counter = 0
    counter = len(file_container)

    # go through all files:
    # FIXME: finish this later.
    for dir_name in file_container:
        file_path = path + dir_name

        for file in file_path:
            if zipfile.is_zipfile(file_path):
                f = zipfile.ZipFile(file_path)
                f.extractall(file_path)
                extract_counter += 1
            else:
                print('{} is not a zip file'.format(file))

    print('Total files contained in this dir:', counter)
    print('Among them, {} files are successfully extracted.'.format(extract_counter))

def try_extract_single_file(destination, path):
    counter = len(path) 
    extract_counter = 0

    if zipfile.is_zipfile(path):
        f = zipfile.ZipFile(path)
        f.extractall(destination)
        extract_counter += 1
    else:
        print(path, 'is not a zip file.')

    print('Total files contained in this dir:', counter)
    print('Among them, {} files are successfully extracted.'.format(extract_counter))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, help='dir path')
    parser.add_argument('--file_name', type=str, help='zip file name')
    parser.add_argument('-s', '--extract_single_file', action='store_true')
    parser.add_argument('-p', '--extract_multi_file', action='store_true')

    # define argument parser:
    opt = parser.parse_args()

    # get zip file dir_path (prefix)
    path = opt.path

    # get zip file's filename:
    zip_file_name = opt.file_name

    print('file path:', path)
    print('filename:', zip_file_name)
    # construct zip file absolute path:
    abs_path = path + '\\' + zip_file_name

    print('abs file path:', abs_path)

    if opt.extract_single_file:
        destination = path + '\\Extracted_files\\'
        try_extract_single_file(destination, abs_path)
    
    if opt.extract_single_file == False and opt.extract_multi_file:
        try_extract_multiple_files(abs_path)