from fastapi import FastAPI


class App(FastAPI):
    ...


def create_app() -> App:
    app = App()

    @app.get("/")
    def root():
        return {"message": "package build_app"}

    return app
