'''
Here are defined views of FastAPI's server:


'''

import os
from app import app
from fastapi import File, UploadFile, Response, status
from file_handling import FileCreator, FileHandler
from tools import Hash, Folder
from starlette.responses import FileResponse
from starlette.requests import Request
from hashlib import md5

STORE_DIR = 'store'



@app.get("/") #NOTE: delete me
async def root():
    return {"message": "Hello World"}



@app.post("/upload/")
async def upload_file(response: Response, file: UploadFile = File(default = None)):

    sub_folder = STORE_DIR
    store_folder = Folder(sub_folder)
    store_folder.prepare()

    file_created, file_name = await FileCreator.create(
        file = file, 
        subdir = sub_folder,
        )

    if file_created:
        response.status_code = 201
        return {'file_name': file_name}
    else:
        response.status_code = 304
        return {'error':'the file already exists', 'file_name': file_name}



@app.get("/download/")
async def download_file(response: Response, file_hash: str = None):

    if not file_hash: #NOTE: doubles from here...
        response.status_code = 400
        return {'error':'file_hash-parameter value required'}

    file = FileHandler(file_hash, sub_dir = STORE_DIR)
    filepath = file.get()
    if not filepath:
        response.status_code = 404
        return {'error': 'file does not exist'} #NOTE: ... to here!

    filename = os.path.split(filepath)[-1]
    response.status_code = 200
    return FileResponse(filepath, filename = filename )



@app.delete("/delete/")
async def delete_file (response: Response, file_hash: str = None):

    if not file_hash: #NOTE: doubles from here...
        response.status_code = 400
        return {'error':'file_hash-parameter value required'}

    file = FileHandler(file_hash, sub_dir = STORE_DIR)
    filepath = file.get()
    if not filepath:
        response.status_code = 404
        return {'error': 'file does not exist'} #NOTE: ... to here!
    
    file_deleted = file.delete()
    if file_deleted:
        response.status_code = 200
        return {'info_message':'file successfully deleted'}
    else:
        response.status_code = 500
        return {'error':'internal server error while trying to delete file'}

