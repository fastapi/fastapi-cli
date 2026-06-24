from fastapi import FastAPI

app = "not a FastAPI instance"
api = 42

my_app = FastAPI()


@my_app.get("/")
def my_app_root():
    return {"message": "my_app"}
