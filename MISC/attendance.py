import os
import sys
import shutil
import logging
import argparse
import pandas as pd
from pyunpack import Archive
from collections import defaultdict

def get_student_info_dict(namelist_path: str, total_lab_counter: int=14):
    """
    This method read namelist and create a container for storing student's id, name and lab submission.
    
    Container Format:
        - STU_ID    : student id.
        - EN_NAME  : student's english name
        - CN_NAME  : student's english name
        - STU_EMAIL : student's email address
        - Lab1, Lab2, ..., Lab13
    """

    # read in namelist from excel file and save them in pd.DataFrame here:
    if namelist_path:
        data = pd.read_excel(namelist_path)
    else:
        # If file not exist:
        logging.error('FILE: \'{}\' not found.'.format(namelist_path))
        sys.exit(0)

    lab_keys      = ['lab' + str(i) for i in range(1, total_lab_counter+1)]        # lab1, lab2, ..., labN
    student_dict  = {}
    stu_eng_names = []

    # Building the student information dictionary:
    for i in range(len(data)):
        # get the i-th student:
        i_th_student = data.iloc[i]

        # loading student information:

        # 1. English name:
        # reverse the eng_name order:
        eng_name = i_th_student['English Name'].split(' ')
        eng_name = ' '.join([eng_name[-1], eng_name[0]])
        eng_name = eng_name.upper()
        stu_eng_names.append(eng_name)

        # chinese name, email, student id
        student_dict[eng_name] = {
            'EN_NAME'   : eng_name,
            'CN_NAME'   : i_th_student['Chinese Name'],
            'STU_EMAIL' : i_th_student['Email'],
            'STU_ID'    : str(i_th_student['Student No'])
        }

        # Initialize lab values here:
        for i in range(len(lab_keys)):
            student_dict[eng_name][lab_keys[i]] = 'No Submission'

    return student_dict, stu_eng_names 

def save_to_excel_file(students: dict, total_lab_counter:int=14):
    """
    This methods save data into excel file:
    """
    lab_keys  = ['lab' + str(i) for i in range(1, total_lab_counter+1)]        # lab1, lab2, ..., labN

    container = {
        'STU_ID': [],
        'EN_NAME': [],
        'CN_NAME': [],
        'STU_EMAIL': [],
    }

    for key in lab_keys:
        container[key] = []


    for i, student in enumerate(students.items()):
        student = student[-1]
        container['EN_NAME'].append(student['EN_NAME'])
        container['CN_NAME'].append(student['CN_NAME'])
        container['STU_ID'].append(student['STU_ID'])
        container['STU_EMAIL'].append(student['STU_EMAIL'])
        for key in lab_keys:
            container[key].append(student[key])

    result = pd.DataFrame(container)
    result.to_excel('result.xlsx')

def get_lab_index(file_name: str):
    """
    This method is used to get the lab index of a downloaded zip file.
    """

    file_name = file_name.lower()

    if 'lab' not in file_name:
        logging.error('FILE: \'{}\' is not a valid downloaded zip file.'.format(file_name))
        return

    index = file_name.index('lab')

    lab_index_prefix = file_name[index+3]
    lab_index_postfix = file_name[index+4]

    try:
        lab_index_post_fix = int(lab_index_postfix)
    except ValueError:
        lab_index_post_fix = ''

    return 'lab' + str(lab_index_prefix) + str(lab_index_postfix)

def unzip_file_to_destination(file_path: str, dest_dir_path: str, lab_index='Lab1'):
    """
    This method is used to unzip file with file_path into dest_dir_path.
    """

    if 'zip' or '7z' or 'rar' in file_name:
        Archive(file_path).extractall(dest_dir_path)
    else:
        logging.error('->[{}] FILE: \'{}\' is not a valid zip file'.format(lab_index, file_name))
        return

def delete_non_zip_files(file_names: list):
    """
    remove invalid file names, and only remain zip file.
    
    - e.g. .DS_store
    """

    for i in range(len(all_lab_zip_files) - 1, -1, -1):
        file_name = all_lab_zip_files[i]

        file_is_zip_file = is_zip_file(file_name)

        if not file_is_zip_file:
            del all_lab_zip_files[i]

def get_student_name(all_name_in_the_name_list: list, dir_name):

    for name in all_name_in_the_name_list:
        if name in dir_name:
            return name

    logging.error('FILE: \'{}\' does not contain valid student name or there\'s sth wrong with the namelist'.format(dir_name))
    sys.exit(0)

def is_zip_file(filename:str) :
    """
    This method is to check if a file with filename is a zip file.
    """
    
    if 'zip' in filename or '7z' in filename or 'rar' in filename:
        return True

    return False

def count_cpp_files(files: list, strict_match=True):
    """
    This method is used to count how many unique c & cpp files is in files.
    """

    unique_cpp_file = []
    counter = 0

    for file in files:

        if '.c' in file or '.cpp' in file:

            if strict_match:
                if file[-3:] == '.c' or file[-4:] == '.cpp':
                    counter += 1
                    unique_cpp_file.append(file)
            else:
                counter += 1
                unique_cpp_file.append(file)

    if counter >= 6:
        print(unique_cpp_file)

    return counter

def get_all_things(path):
    """
    This method is used to get all stuffs (including plain files and folders) under a path.
    """
    
    normal_files = []
    zip_files = []
    dirs = []

    for r, d, f in os.walk(path, topdown=False):
        for name in f:
            # check if this is a hidden file:
            if name[:2] == '._':
                continue

            # not a hidden file, then:
            if is_zip_file(name):
                zip_files.append(os.path.join(r, name))
            else:
                normal_files.append(os.path.join(r, name))

        for name in d:
            dirs.append(os.path.join(r, name))

    return normal_files, zip_files, dirs

if __name__ == '__main__':
    # Define logger:
    logging.basicConfig(format='[%(asctime)s] %(levelname)s -> %(message)s', level=logging.INFO)

    # Define argument parser:
    parser = argparse.ArgumentParser()

    parser.add_argument('-L', '--loose', action='store_true', help='Adopt loose counting scheme.')
    parser.add_argument('-T', '--total_lab_counter', type=int, help='Indicate the total amount of lab, e.g. 14.')

    opts = parser.parse_args()

    # by default, the namelist file should be placed in the same place as this py file.
    students, student_names = get_student_info_dict(namelist_path='./namelist.xls')

    lower_student_names = [name.lower() for name in student_names]

    # get all files here:
    # ---------------------------------------------------------------------------
    root_path = os.path.abspath('.')

    # define dir used to store all downloaded lab zip files here:
    lab_dir_name = 'labs'
    lab_source_path = os.path.join(root_path, lab_dir_name)
    
    # get all lab zip files:
    all_lab_zip_files = sorted(os.listdir(lab_source_path))

    # remove invalid files:
    delete_non_zip_files(all_lab_zip_files)

    # store all unzipped results:
    intermediate_dir_name = 'TEMP'
    intermediate_dir_path = os.path.join(lab_source_path, intermediate_dir_name)
    # mk a temp dir here:
    os.mkdir(intermediate_dir_path)

    for file in all_lab_zip_files:
        lab_x = get_lab_index(file)
        lab_x_submission_counter = 0

        # unzip to corresponding lab_x dir:
        lab_x_temp_path = os.path.join(intermediate_dir_path, lab_x)
        os.mkdir(lab_x_temp_path)

        unzip_file_to_destination(os.path.join(lab_source_path, file), lab_x_temp_path, lab_index=lab_x)

        # ---------------------------------------------------------------------------
        # get all submitted files for this lab:
        all_submitted_files_for_lab_x = sorted(os.listdir(lab_x_temp_path))

        for each_submission_dir in all_submitted_files_for_lab_x:
            # used to store valid cpp_or_c file submission.
            cpp_submission_counter = None

            # get this student's english name here:
            stu_name = get_student_name(lower_student_names, each_submission_dir.lower())

            # get all files and folders under this path:
            stu_submission_zip_file_path = os.path.join(lab_x_temp_path, each_submission_dir)
            normal_files, zip_files, dirs = get_all_things(stu_submission_zip_file_path)

            if len(zip_files) > 0:
                result_dir_path = os.path.join(stu_submission_zip_file_path, 'result')
                os.mkdir(result_dir_path)

                for z_file in zip_files:
                    unzip_file_to_destination(z_file, result_dir_path)

            # start counting valid cpp files:
            normal_files, zip_files, dirs = get_all_things(stu_submission_zip_file_path)

            cpp_submission_counter = count_cpp_files(normal_files, strict_match=(not opts.loose))

            students[stu_name.upper()][lab_x.strip()] = cpp_submission_counter

            logging.info('[{}]: student name: {}, valid submission: {}'.format(lab_x.upper().strip(), stu_name, cpp_submission_counter))

            lab_x_submission_counter += 1

        logging.info('Total submission for {}: {}; Total students: {}'.format(lab_x, lab_x_submission_counter, len(lower_student_names)))
        logging.info('-'*50)

    # save submission log into excel file:
    save_to_excel_file(students)

    # remove the temp file
    shutil.rmtree(intermediate_dir_path)
