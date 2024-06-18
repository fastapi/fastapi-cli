from fastapi import FastAPI


class App(FastAPI): ...


def create_app_other() -> App:
    app = App()

    @app.get("/")
    def app_root():
        return {"message": "single file factory app inherited"}

    return app


def create_app() -> FastAPI:
    app = FastAPI()

    @app.get("/")
    def app_root():
        return {"message": "single file factory app"}

    return app
