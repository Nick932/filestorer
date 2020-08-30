'''
This module implements few classes for some work with files:

DeleteFile - to delete it;
GiveFile - to return it;
UploadFile - the class to upload file.
'''

import os,sys
import shutil
from tools import Folder
from fastapi import UploadFile
from hashlib import md5



class FileHandler:
    '''
    This class finds file by it's name and implements next methods:
    get - returns the absolute filepath and it's name+type.
    delete - removes the file.
    '''
    def __init__(self, file_name:str, sub_dir:str = ''):

        self.cwd = os.getcwd()
        self.filename = file_name
        self.subdir = sub_dir
        self.subdir_path = os.path.join(self.cwd, self.subdir)
        self.filedir = self.filename[:2]

    def _find(self):

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
        
        return file


    def get(self):
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
        '''
        Creates a file using UploadFile object from fastapi.

        Expected next arguments:
        file (bytes) - an UploadFile object.
        subdir (str) - the optional sub directory for the file.

        Returns 1 and name of the file, if the file was created or 
        0 and name of the file, if it is already exist.
        '''

        file_type = file.filename.split('.')[-1]

        temp_folder_name = 'tempfolder'
        temp_folder_path = os.path.join(subdir, temp_folder_name)
        temp_folder = Folder(temp_folder_path)
        temp_folder.prepare()

        temp_file_name = 'tempfile'
        temp_file_path = os.path.join(temp_folder_path,temp_file_name)
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
        filename = '.'.join([the_hash, file_type]) #TODO: make tests for final hash
        sub_folder_name = filename[:2]
        sub_folder_path = os.path.join(subdir, sub_folder_name)

        # If the file already exists:
        if sub_folder_name in os.listdir(subdir):
            if filename in os.listdir(sub_folder_path):
                shutil.rmtree(temp_folder_path)
                return 0, filename

        # Rename the exiting temp file:
        renamed_file_path = os.path.join(temp_folder_path, filename)
        os.rename(os.path.join(temp_folder_path, temp_file_name), renamed_file_path)

        # Rename temp folder:
        shutil.move(temp_folder_path, sub_folder_path)

        return 1, filename



FileCreator = CreateFile()