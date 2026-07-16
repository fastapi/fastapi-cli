import os

from fastapi import FastAPI

app = FastAPI()

fastapi_env_at_import = os.environ.get("FASTAPI_ENV")


@app.get("/fastapi-env")
def get_fastapi_env() -> dict[str, str | None]:
    return {"fastapi_env": fastapi_env_at_import}
