from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def app_root():
    return {"message": "single file app"}
