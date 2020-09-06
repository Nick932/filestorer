'''
This module implements few classes for some work with files:


CreateFile - this class creates file and returns result status and file's name;

FileHandler - to get a file path or delete a file;

FileInteractor - the class for file management: includes info about file's
    status, path to the file, and error message data (for example, if file 
    doesn't exist).
'''

from logger import logger

import os,sys
import shutil
from tools import Folder
from tools import Status as status
from fastapi import UploadFile
from hashlib import md5

STORE_DIR = 'store'



class FileHandler:
    '''
    This class finds file by it's name and implements next methods:

    get - returns the absolute filepath and it's name+type.
    delete - removes the file.

    :param file_name: the name of the file to work with.
    :type file_name: str

    :param sub_dir: the name of necessary sub directory to
    store the file. Defaults to None (file will be storred in current
    directory).
    :type sub_dir: str 
    '''
    def __init__(self, file_name:str, sub_dir:str = ''):

        self.cwd = os.getcwd()
        self.filename = file_name
        self.subdir = sub_dir
        self.subdir_path = os.path.join(self.cwd, self.subdir)
        self.filedir = self.filename[:2]
        logger.info('sub dir path:\n{0}\n'.format(self._subdir_path))

    def _find(self):
        '''
        Finds the file, that specified like self.filename.

        :return: full file path + file name.
        :rtype: str
        ''' 

        if self.subdir:
            if not self.filedir in os.listdir(self.subdir_path):
                return None
        path_to_filedir = os.path.join(self.subdir, self.filedir)

        full_name = None
        filedir_content = os.listdir(path_to_filedir)
        for obj in filedir_content:
            if self.filename in obj:
                full_name = obj
        if full_name == None:
            return None

        file = os.path.abspath(os.path.join(path_to_filedir, full_name))
        logger.info('file path:\n{0}\n'.format(file))
        
        return file


    def get_path(self):
        '''Returns the absolute file path + filename + filetype.'''

        file = self._find()

        return file


    def delete(self):
        '''Deletes the file.
        Returns True, if the file was succesfully deleted.
        '''

        file = self._find()
        os.remove(file)

        return True



class CreateFile:
    '''
    This class handles file uploads by users.
    
    Creates a file and calculates it's hash.
    ''' 
    async def create(
        self, 
        file:UploadFile, 
        subdir:str = ''):
        '''Creates a file using UploadFile object from fastapi.

        Expected next arguments:

        :param file: An UploadFile object
        :type file: bytes
        
        :param subdir: The optional sub directory for the file.
        :type subdir: str

        :return: Status.done.value and name of the file, if the 
        file was created or status.exists.value and name of the file, 
        if it is already exist.
        :rtype: tuple(str, str)
        '''

        file_type = file.filename.split('.')[-1]

        temp_folder_name = 'tempfolder'
        temp_folder_path = os.path.join(subdir, temp_folder_name)
        logger.info('temp folder path:\n{0}\n'.format(temp_folder_path))
        temp_folder = Folder(temp_folder_path)
        temp_folder.prepare()

        temp_file_name = 'tempfile'
        temp_file_path = os.path.join(temp_folder_path,temp_file_name)
        logger.info('temp file path:\n{0}\n'.format(temp_file_path))
        temp_file = open(temp_file_path, 'wb')
        hash_code = md5()


        while True:

            chunk = await file.read(20000)

            if not chunk:
                break

            hash_code.update(chunk)
            temp_file.write(chunk)
        

        temp_file.close()
        the_hash = hash_code.hexdigest()
        filename = '.'.join([the_hash, file_type])
        sub_folder_name = filename[:2]
        sub_folder_path = os.path.join(subdir, sub_folder_name)
        logger.info('sub folder path:\n{0}\n'.format(sub_folder_path))

        # If the file already exists?
        if sub_folder_name in os.listdir(subdir):
            if filename in os.listdir(sub_folder_path):
                shutil.rmtree(temp_folder_path)
                return status.exists.value, filename

        # Rename the exiting temp file:
        renamed_file_path = os.path.join(temp_folder_path, filename)
        logger.info('renamed file path:\n{0}\n'.format(renamed_file_path))
        os.rename(os.path.join(temp_folder_path, temp_file_name), renamed_file_path)

        # Rename the temp folder:
        shutil.move(temp_folder_path, sub_folder_path)
        logger.info('renamed dir path:\n{0}\n'.format(sub_folder_path))

        return status.done.value, filename


class FileInteractor:
    '''The interface to an exiting file.


    :param str file_hash: A hash of the file, which is used like file's name

    :var int HTTP_status_code: An instance's attribute which contains the HTTP
    status code.

    :var error_message: An instance's attribute which returns None or dict with
    only one 'error' key, which value is the error message (str).
    :type error_message: None or dict

    :var file: A :class: 'FileHandler' object, which gives us it's methods
    like 'delete'::
        FileInteractor.file.delete() # will delete the file.
    :type file: FileHandler

    :var str file_path: A full file path + file name.

    '''    

    def __init__(self, file_hash):

        self.HTTP_status_code = 200
        self.error_message = None
        self.file_hash = file_hash

        if not self.file_hash:
            self.HTTP_status_code = 400
            self.error_message = {'error':'file_hash-parameter value required'}

        self.file = FileHandler(self.file_hash, sub_dir = STORE_DIR)
        self.file_path = self.file.get_path()

        if not self.file_path:
            self.HTTP_status_code = 404
            self.error_message = {'error': 'file does not exist'}


FileCreator = CreateFile()