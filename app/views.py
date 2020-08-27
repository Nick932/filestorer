'''
Here are defined views of FastAPI's server:


'''



from app import app
from fastapi import File, UploadFile
from file_handling import FileCreator
from tools import Hash, Folder
import glob



@app.get("/") #NOTE: delete me
async def root():
    return {"message": "Hello World"}



@app.post("/upload/")
async def upload_file(file: UploadFile = File(default = None)):

    file_bytes = await file.read()

    hasher = Hash(file_bytes)
    filename = hasher.get_hash()

    filetype = file.filename.split('.')[-1]

    await file.close()

    file_folder = filename[:2]

    folder_creator = Folder(file_folder)
    folder_creator.prepare()

    file_created = FileCreator.create(
        file_bytes = file_bytes, 
        file_name = filename, 
        file_type = filetype,
        subdir = file_folder,
        )
    
    if file_created:
        return {'file_name': filename}
    else:
        return {'error':'the file already exists', 'file_name': filename}



@app.get("/download/")
async def download_file(file_hash: str = None): #TODO: find the dir with first 2 symbols of the hash

    if not file_hash:
        return {'error':'file_hash-parameter value required'}
        
    file_name = str(file_hash)
    search_query = file_name+'.*'
    print(glob.glob('*'), search_query)

