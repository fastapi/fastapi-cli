from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI()

    @app.get("/")
    def root():
        return {"message": "package create_app"}

    return app
