'''
Here are defined views of FastAPI's server:


'''



from app import app
from fastapi import File, UploadFile
from file_handling import FileCreator
from tools import Hasher, Folder



@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.post("/upload/")
async def upload_file(file: UploadFile = File(default = None)):

    file_bytes = await file.read()
    filename = Hasher.get_hash(file_bytes)
    filetype = file.filename.split('.')[-1]
    await file.close()

    file_folder = filename[:2]

    folder_creator = Folder(file_folder)
    folder_creator.prepare()

    file_created = FileCreator.create(
        file_bytes = file_bytes, 
        filename = filename, 
        filetype = filetype,
        subdir = file_folder,
        )
    
    if file_created:
        return {'file_name': filename}
    else:
        return{'error':'internal server error while creating file'}
