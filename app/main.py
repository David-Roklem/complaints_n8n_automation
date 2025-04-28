import asyncio
import uvicorn
from fastapi import FastAPI
import router
from database import db_helper

app = FastAPI()
app.include_router(router.router)

if __name__ == "__main__":
    asyncio.run(db_helper.create_tables())
    uvicorn.run("main:app", host="api", reload=True)
    # uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
