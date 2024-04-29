from fastapi import FastAPI

first_other = FastAPI()


@first_other.get("/")
def first_other_root():
    return {"message": "single file first_other"}


second_other = FastAPI()


@second_other.get("/")
def second_other_root():
    return {"message": "single file second_other"}


api = FastAPI()


@api.get("/")
def api_root():
    return {"message": "single file api"}


app = FastAPI()


@app.get("/")
def app_root():
    return {"message": "single file app"}
