'''
Here are defined views of FastAPI's server:


'''



from app import app



@app.get("/")
async def root():
    return {"message": "Hello World"}
