from fastapi import FastAPI, Depends
# from multimethod import RETURN

app=FastAPI()

@app.get("/")
async def first_api_start():
    return {'message': "Hello World!"}

# @app.get("/")
# async def first_api_start(key):
#     return {'message': f"Hello World!  {key}"}
