import unittest
from file_handling import CreateFile
from hashlib import md5
import os
from logger import logger


class hashingTests(unittest.TestCase):
    '''Tests the hashing process.'''

    def setUp(self):

        cwd = os.getcwd()
        self.temp_file_path = os.path.join(cwd, 'temp_test_file')
        self.example_file_name = os.path.join(cwd, 'hashing_test_file')

        self.example_file = open(self.example_file_name, 'wb')
        self.example_file.write(b'example'*20000)
        self.example_file.close()
        self.example_file = open(self.example_file_name, 'rb')


    def hash_by_chunk(self, file):
        '''
        Expects full file path like 'file'-argument.

        Writes it chunk by chunk in the new file, 
        creates hash of the file in parallel.
        '''

        file = open(file, 'rb')
        hash_code = md5()
        temp_file = open(self.temp_file_path, 'wb')

        while True:

            chunk = file.read(2000)

            if not chunk:
                break

            hash_code.update(chunk)
            temp_file.write(chunk)
        
        file.close()
        temp_file.close()

        return hash_code.hexdigest()

        
    def test_chunk_by_chunk_hashing(self):
        '''Tests the result of 'chunk by chunk' hashing.'''


        hashing_chunk_by_chunk = self.hash_by_chunk(self.example_file_name)
        hashing_entire_file = md5(self.example_file.read()).hexdigest()
        logger.info(
            'Hash chunk by chunk:\n'+
            str(hashing_chunk_by_chunk)+
            '\nHash of the entire file:\n'+
            str(hashing_entire_file)
            )

        self.assertEqual(
            hashing_chunk_by_chunk, 
            hashing_entire_file,
        )
    

    def tearDown(self):

        for file in [self.temp_file_path, self.example_file_name,]:
            os.remove(file)
        self.example_file.close()



if __name__ == '__main__':
    unittest.main()