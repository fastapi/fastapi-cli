from fastapi import FastAPI

application = FastAPI()


@application.get("/")
def app_root():
    return {"message": "configured app"}
