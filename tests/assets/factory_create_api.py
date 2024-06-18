from fastapi import FastAPI


def create_api() -> FastAPI:
    app = FastAPI()

    @app.get("/")
    def app_root():
        return {"message": "single file factory app"}

    return app
