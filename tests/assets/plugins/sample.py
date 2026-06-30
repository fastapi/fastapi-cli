import typer


def register(app: typer.Typer) -> None:
    @app.command("ping")
    def ping() -> None:
        """Test command added by plugin."""
        typer.echo("pong")  # pragma: no cover
