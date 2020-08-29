'''
Here are defined views of FastAPI's server:


'''
#FIXME: везде: если папка\файл not found, возвращать 404!

import os
from app import app
from fastapi import File, UploadFile
from file_handling import FileCreator, FileHandler
from tools import Hash, Folder
from starlette.responses import StreamingResponse, FileResponse
from starlette.requests import Request
from hashlib import md5

STORE_DIR = 'store'



@app.get("/") #NOTE: delete me
async def root():
    return {"message": "Hello World"}



@app.post("/upload/")
async def upload_file(file: UploadFile = File(default = None)):

    sub_folder = STORE_DIR
    store_folder = Folder(sub_folder)
    store_folder.prepare()

    file_created, file_name = await FileCreator.create(
        file = file, 
        subdir = sub_folder,
        )

    if file_created:
        return {'file_name': file_name}
    else:
        return {'error':'the file already exists', 'file_name': file_name}



@app.get("/download/")
async def download_file(file_hash: str = None):

    if not file_hash: #NOTE: doubles!
        return {'error':'file_hash-parameter value required'} #NOTE: doubles!

    file = FileHandler(file_hash, sub_dir = STORE_DIR) #NOTE: doubles!
    if not file: #NOTE: doubles!
        return {'error': 'file does not exist'} #NOTE: doubles!
    file = open(file.get(), 'rb')

    return StreamingResponse(file)



@app.delete("/delete/")
async def delete_file (file_hash: str = None):

    if not file_hash: #NOTE: doubles!
        return {'error':'file_hash-parameter value required'} #NOTE: doubles!

    file = FileHandler(file_hash, sub_dir = STORE_DIR) #NOTE: doubles!
    if not file: #NOTE: doubles!
        return {'error': 'file does not exist'} #NOTE: doubles!
    file_deleted = file.delete()

    if file_deleted:
        return {'info_message':'file successfully deleted'}
