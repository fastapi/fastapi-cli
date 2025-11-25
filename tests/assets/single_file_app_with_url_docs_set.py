from fastapi import FastAPI

app = FastAPI(docs_url="/my-custom-docs-path")


@app.get("/")
def api_root():
    return {"message": "my FastAPI app with a custom docs path"}
