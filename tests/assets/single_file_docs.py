from fastapi import FastAPI

# App 1: API documentation disabled via `openapi_url=None`
# ------------------------------------------------------------------------------------

openapi_none = FastAPI(openapi_url=None)


@openapi_none.get("/")
def openapi_none_root():
    return {"message": "single file openapi_none"}


# App 2: Both docs and redoc disabled via `docs_url=None` and `redoc_url=None`
# ------------------------------------------------------------------------------------

docs_none_redoc_none = FastAPI(docs_url=None, redoc_url=None)


@docs_none_redoc_none.get("/")
def docs_none_redoc_none_root():
    return {"message": "single file docs_none_redoc_none"}


# App 3: Only ReDoc. Swagger docs disabled via `docs_url=None`
# ------------------------------------------------------------------------------------

only_redoc = FastAPI(docs_url=None)


@only_redoc.get("/")
def only_redoc_root():
    return {"message": "single file only_redoc"}


# App 4: Only Swagger docs. ReDoc disabled via `redoc_url=None`
# ------------------------------------------------------------------------------------

only_docs = FastAPI(redoc_url=None)


@only_docs.get("/")
def only_docs_root():
    return {"message": "single file only_docs"}


# App 5: Both docs and redoc enabled with default URLs
# ------------------------------------------------------------------------------------

full_docs = FastAPI()


@full_docs.get("/")
def full_docs_root():
    return {"message": "single file full_docs"}


# App 6: Swagger docs with custom URL. ReDoc with default URL.
# ------------------------------------------------------------------------------------

custom_docs = FastAPI(docs_url="/custom-docs-url")


@custom_docs.get("/")
def custom_docs_root():
    return {"message": "single file custom_docs"}


# App 7: ReDoc with custom URL. Swagger docs with default URL.
# ------------------------------------------------------------------------------------

custom_redoc = FastAPI(docs_url=None, redoc_url="/custom-redoc-url")


@custom_redoc.get("/")
def custom_redoc_root():
    return {"message": "single file custom_redoc"}
