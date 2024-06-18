from fastapi import FastAPI
from fastapi_cli.discover import check_factory


def test_check_untyped_factory() -> None:
    def create_app():  # type: ignore[no-untyped-def]
        return FastAPI()  # pragma: no cover

    assert check_factory(create_app) is False


def test_check_typed_factory() -> None:
    def create_app() -> FastAPI:
        return FastAPI()  # pragma: no cover

    assert check_factory(create_app) is True


def test_check_typed_factory_inherited() -> None:
    class MyApp(FastAPI):
        ...

    def create_app() -> MyApp:
        return MyApp()  # pragma: no cover

    assert check_factory(create_app) is True


def test_create_app_with_different_type() -> None:
    def create_app() -> int:
        return 1  # pragma: no cover

    assert check_factory(create_app) is False
