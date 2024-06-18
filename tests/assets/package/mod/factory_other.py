from fastapi import FastAPI


def build_app() -> FastAPI:
    app = FastAPI()

    @app.get("/")
    def root():
        return {"message": "package build_app"}

    return app
