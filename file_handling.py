'''
This module implements few classes for some work with files:

DeleteFile - to delete it;
GiveFile - to return it;
UploadFile - the class to upload file.
'''

import os
from tools import Folder


class FindFile:
    '''
    This class implements the basic method for
    inner use: it finds file by it's name.
    '''
    def __init__(self, filename:str, subdir:str = None):
        self.filename = filename



class GiveFile(FindFile):
    '''
    This class returns the file with the given 
    name.
    '''
    def get():
        '''Returns the file.'''



class DeleteFile(FindFile):
    '''
    This class deletes the file with the given
    name.
    '''
    def delete():
        '''Deletes the file.'''



class CreateFile:
    '''
    This class handles file uploads by users.
    ''' 
    def create(self, file_bytes:bytes, file_name:str, file_type:str, subdir:str = None):
        '''
        Creates a file using file bytes.

        Expected next arguments:
        file_bytes (bytes) - an array of file's bytes.
        file_name (str) - the name of the file, excluding the format of a file.
        file_type (str) - a type of the file.
        subdir (str) - the optional sub directory for the file.

        Returns True, if the file was created or False, if it's already exist.
        '''
        full_file_name = file_name+'.'+file_type
        cwd = None

        if subdir:
            os.chdir(subdir)

        if full_file_name in os.listdir():
            return False

        file_obj = open(full_file_name, 'wb')
        file_obj.write(file_bytes)
        file_obj.close()

        if cwd:
            os.chdir(cwd)

        return True



FileCreator = CreateFile()