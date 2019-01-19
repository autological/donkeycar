"""
Utilities to manipulate files and directories.
"""

import glob
import zipfile
import os
import tensorflow as tf

from ..log import get_logger

logger = get_logger(__name__)

def most_recent_file(dir_path, ext=''):
    """
    return the most recent file given a directory path and extension
    """
    query = dir_path + '/*' + ext
    newest = min(glob.iglob(query), key=os.path.getctime)
    return newest


def make_dir(path):
    real_path = os.path.expanduser(path)
    if not os.path.exists(real_path):
        os.makedirs(real_path)
    return real_path


def zip_dir(dir_path, zip_path):
    """
    Create and save a zipfile of a one level directory
    """
    file_paths = glob.glob(dir_path + "/*")  # create path to search for files.

    zf = zipfile.ZipFile(zip_path, 'w')
    dir_name = os.path.basename(dir_path)
    for p in file_paths:
        file_name = os.path.basename(p)
        zf.write(p, arcname=os.path.join(dir_name, file_name))
    zf.close()
    return zip_path


def time_since_last_file_edited(path):
    """return seconds since last file was updated"""
    list_of_files = glob.glob(os.path.join(path, '*'))
    if len(list_of_files) > 0:
        latest_file = max(list_of_files, key=os.path.getctime)
        return int(time.time() - os.path.getctime(latest_file))
    return 0



def expand_path_mask(path):
    matches = []
    path = os.path.expanduser(path)
    print("The expanded path for this tub is: {}".format(path))
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/wes/.ssh/saddle-210105-78307d457b87.json'
    if path.startswith('gs://'):
        for file in tf.gfile.Glob(path):
            print("Found file: {}".format(file))
            # if tf.gfile.IsDirectory(file):
            #     matches.append(os.path.join(os.path.abspath(file)))
                # matches.append(os.path.join(file) # Alternatively
    else:
        for file in glob.glob(path):
            if os.path.isdir(file):
                matches.append(os.path.join(os.path.abspath(file)))
    return matches

def expand_path_arg(path_str):
    path_list = path_str.split(",")
    expanded_paths = []
    for path in path_list:
        paths = expand_path_mask(path)
        expanded_paths += paths
    return expanded_paths
