from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def api_root():
    return {"message": "any message"}
