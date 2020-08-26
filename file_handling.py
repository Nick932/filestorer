'''
This module implements few classes for some work with files:

DeleteFile - to delete it;
GiveFile - to return it;
UploadFile - the class to upload file.
'''

import os



class FindFile:
    '''
    This class implements the basic method for
    inner use: it finds file by it's name.
    '''
    def __init__(self, filename):
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
    def run():
        '''Deletes the file.'''



class CreateFile:
    '''
    This class handles file uploads by users.
    ''' 
    def create(self, file_bytes:bytes, file_name:str, file_type:str, subdir:str = None):
        '''
        Creates a file using file bytes.

        Expected next arguments:


        Returns True, if the file was created or False, if not.
        '''
        filename = file_name+'.'+file_type
        cwd = None

        if subdir:
            cwd = os.getcwd()
            os.mkdir(os.sep+subdir)
            os.chdir(os.sep+subdir)

        file_obj = open(filename, 'wb')
        file_obj.write(file_bytes)
        file_obj.close()

        if cwd:
            os.chdir(cwd)

        return True



FileCreator = CreateFile()