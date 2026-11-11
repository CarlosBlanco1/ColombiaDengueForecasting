from fastapi import FastAPI
from routers.predictions import router as p_router

app = FastAPI()

app.include_router(p_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}




    

    


