from fastapi import FastAPI

app = FastAPI(docs_url="/my-custom-docs-path", root_path="/api/v1")


@app.get("/")
def api_root():
    return {"message": "my FastAPI app with a custom docs path and root path"}
