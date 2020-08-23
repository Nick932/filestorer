'''
This module implements few classes for some work with files:

DeleteFile - to delete it;
GiveFile - to return it;
UploadFile - the class to upload file.
'''



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



class UploadFile:
    '''
    This class handles file uploads by users.
    ''' 