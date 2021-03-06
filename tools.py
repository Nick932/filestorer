'''
This module implements next instruments:

- class 'Folder' - to create new folders.
- class 'Hash' - to create hashes.

'''

from hashlib import md5
import os, sys
import enum



class Folder:
    '''Preparing folder. Creates folder if it doesn't exists.
    Open methods defined here:
    prepare() - to start the process of folder's creating.
    
    Takes 1 argument:
    - foldername (in str format) - name of the necessary folder.
    '''
    
    def __init__(self, foldername : str):
        
        self.foldername = foldername
        
        if not isinstance(self.foldername, str):
            raise TypeError('Incorrect type of foldername: it must be str.')
            
    
    def _folder_already_exists(self, foldername : str, current_directory : str):
        '''Checks if folder with such name already exists.
        
        Takes 2 arguments:
        - foldername (in str format) - name of necessary folder;
        - current_directory (in str format) - path to the current working
          directory.
          
        Returns True or False.
        '''
        
        cwd = current_directory
        
        # Create list of folders in current working directory.
        cwd_folders = [ object for object in os.listdir(cwd) if os.path.isdir(cwd+os.sep+object) ]
        
        return foldername in cwd_folders    
            
            
    def _create_folder(self, foldername : str,  current_directory : str):
        '''Creates a folder in the given directory.
        
        Takes 2 arguments:
        - foldername (in str format) - name of the necessary folder;
        - current_directory (in str format) - the necessary directory
          for the folder.
       ''' 
        
        cwd = current_directory
        
        try:
            os.mkdir(cwd+os.sep+foldername)
        except PermissionError as exception:
            raise exception('You have no permissions to create a folder in this directory:\n'+cwd)
        except Exception as exception:
            print('Some unhandled error has occured:\n', sys.exc_info()[1])
            raise exception
    
    
    def prepare(self):
        '''Checks if the folder already exists. If not, creates it.
        
        Delegates both of these processes to internal methods.
        Defines the current working directory for passing it to
        these internal methods like argument.
        '''
        
        cwd = os.getcwd()
        if not self._folder_already_exists(self.foldername,  cwd):
            self._create_folder(self.foldername,  cwd)



class Status(enum.Enum):
  done = 'statusdone'
  failed = 'statusfailed'
  exists = 'statusexists'
