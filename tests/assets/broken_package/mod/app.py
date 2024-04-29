from fastapi import FastAPI

from ..utils import get_message

app = FastAPI()


@app.get("/")
def app_root():
    return {"message": get_message()}
