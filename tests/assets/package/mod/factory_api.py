from fastapi import FastAPI


def create_api() -> FastAPI:
    app = FastAPI()

    @app.get("/")
    def root():
        return {"message": "package create_api"}

    return app
