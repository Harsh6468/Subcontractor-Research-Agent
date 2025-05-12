from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
import uvicorn
from api.routes import router

app = FastAPI()

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)