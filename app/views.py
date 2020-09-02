'''
Here are defined views of FastAPI's server.
'''

import os
from app import app
from fastapi import File, UploadFile, Response, status
from file_handling import FileCreator, FileHandler, FileInteractor, STORE_DIR
from tools import Hash, Folder
from tools import Status as status
from starlette.responses import FileResponse
from starlette.requests import Request
from hashlib import md5



@app.post("/upload/")
async def upload_file(response: Response, file: UploadFile = File(default = None)):

    sub_folder = STORE_DIR
    store_folder = Folder(sub_folder)
    store_folder.prepare()

    state, file_name = await FileCreator.create(
        file = file, 
        subdir = sub_folder,
        )

    if state == status.done.value:
        response.status_code = 201
        return {'file_name': file_name}
    if state == status.exists.value:
        response.status_code = 304
        return {'error':'the file already exists', 'file_name': file_name}



@app.get("/download/")
async def download_file(response: Response, file_hash: str = None):

    data = FileInteractor(file_hash)

    if data.error_message:
        response.status_code = data.HTTP_status_code
        return data.error_message

    filepath = data.file_path
    filename = os.path.split(filepath)[-1]
    response.status_code = data.HTTP_status_code

    return FileResponse(filepath, filename = filename )



@app.delete("/delete/")
async def delete_file (response: Response, file_hash: str = None):

    data = FileInteractor(file_hash)
    if data.error_message:
        response.status_code = data.HTTP_status_code
        return data.error_message
    
    file_deleted = data.file.delete()
    if file_deleted:
        response.status_code = data.HTTP_status_code
        return {'info_message':'file successfully deleted'}
    else:
        response.status_code = 500
        return {'error':'internal server error while trying to delete file'}

