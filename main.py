import uvicorn
from fastapi import FastAPI

from api.handlers import router

app = FastAPI(title="sirius")

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
