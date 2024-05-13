from fastapi import FastAPI

app = FastAPI(docs_url=None)


@app.get("/")
def api_root():
    return {"message": "any message"}
