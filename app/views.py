'''
Here are defined views of FastAPI's server:


'''
#FIXME: везде: если папка\файл not found, возвращать 404!

import os
from app import app
from fastapi import File, UploadFile
from file_handling import FileCreator, FindFile
from tools import Hash, Folder
from starlette.responses import StreamingResponse, FileResponse
from starlette.requests import Request



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

    file_folder = filename[:2] #FIXME: correct path is: store/ab/filename !

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
async def download_file(file_hash: str = None):

    if not file_hash:
        return {'error':'file_hash-parameter value required'} #NOTE: doubles!

    fileobj = FindFile(file_hash, sub_dir = file_hash[:2])
    file = open(fileobj.get(), 'rb')

    return StreamingResponse(file)



@app.delete("/delete/")
async def delete_file (file_hash: str = None):

    if not file_hash:
        return {'error':'file_hash-parameter value required'} #NOTE: doubles!

    file = FindFile(file_hash, sub_dir = file_hash[:2])
    file_deleted = file.delete()

    if file_deleted:
        return {'info_message':'file successfully deleted'}
