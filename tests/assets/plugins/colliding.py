import typer


def register(app: typer.Typer) -> None:
    @app.command("dev")  # collides with built-in dev command
    def dev() -> None:
        pass  # pragma: no cover
