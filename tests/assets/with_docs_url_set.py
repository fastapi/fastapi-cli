from fastapi import FastAPI

app = FastAPI(docs_url="/any-other-path")


@app.get("/")
def api_root():
    return {"message": "any message"}
